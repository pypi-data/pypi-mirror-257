import torch
from ring_attention_pytorch import RingAttention
from torch import Tensor, nn
from torch.nn import Module
from zeta.nn import FeedForward, audio_to_text, img_to_text, video_to_text, OutputHead
from zeta.structs import AutoregressiveWrapper

from gemini_torch.transformer import Decoder, Transformer


def exists(val):
    return val is not None


class LongGeminiTransformerBlock(nn.Module):
    """
    Gemini15TransformerBlock is a transformer block used in the Gemini15 model.

    Args:
        dim (int): The input dimension of the block.
        depth (int, optional): The depth of the block. Defaults to 32.
        dim_head (int, optional): The dimension of each head in the multi-head attention mechanism. Defaults to 128.
        heads (int, optional): The number of attention heads. Defaults to 24.
        use_abs_pos_emb (bool, optional): Whether to use absolute positional embeddings. Defaults to False.
        attn_flash (bool, optional): Whether to use flash attention. Defaults to True.
        attn_kv_heads (int, optional): The number of heads to use for key-value attention. Defaults to 2.
        qk_norm (bool, optional): Whether to apply layer normalization to query, key, and value. Defaults to True.
        ff_mult (int, optional): The multiplier for the hidden dimension in the feedforward network. Defaults to 4.

    Attributes:
        dim (int): The input dimension of the block.
        depth (int): The depth of the block.
        dim_head (int): The dimension of each head in the multi-head attention mechanism.
        heads (int): The number of attention heads.
        use_abs_pos_emb (bool): Whether to use absolute positional embeddings.
        attn_flash (bool): Whether to use flash attention.
        attn_kv_heads (int): The number of heads to use for key-value attention.
        qk_norm (bool): Whether to apply layer normalization to query, key, and value.
        attn (RingAttention): The attention model for the block.
        norm (nn.LayerNorm): The layer normalization module.
        ffn (FeedForward): The feedforward model for the block.

    """

    def __init__(
        self,
        dim: int,
        depth: int = 32,
        dim_head: int = 128,
        heads: int = 24,
        qk_norm: bool = True,
        ff_mult: int = 4,
        ring_seq_size: int = 512,
        *args,
        **kwargs,
    ):
        super().__init__()
        self.dim = dim
        self.depth = depth
        self.dim_head = dim_head
        self.heads = heads
        self.qk_norm = qk_norm
        self.ff_mult = ff_mult
        self.ring_seq_size = ring_seq_size

        # Attention model for the block
        self.attn = RingAttention(
            dim=dim,
            dim_head=dim_head,
            heads=True,
            causal=True,
            auto_shard_seq=True,
            ring_attn=True,
            ring_seq_size=ring_seq_size,
            prenorm=True,
            *args,
            **kwargs,
        )

        # Post Attention layer normalization
        self.norm = nn.LayerNorm(dim)

        # Feedforward model for the block
        self.ffn = FeedForward(dim, dim, ff_mult, *args, **kwargs)

    def forward(self, x: Tensor, *args, **kwargs):
        """
        Forward pass of the Gemini15TransformerBlock.

        Args:
            x (Tensor): The input tensor.

        Returns:
            Tensor: The output tensor.

        """
        x = self.norm(x)

        # Attention
        x = self.attn(x)

        # Feedforward
        x = self.ffn(x) + x

        return x


class LongGemini(nn.Module):
    """
    LongGemini model implementation.

    Args:
        dim (int): Dimension of the input.
        depth (int, optional): Depth of the model. Defaults to 32.
        dim_head (int, optional): Dimension of each head. Defaults to 128.
        long_gemini_depth (int, optional): Depth of the LongGemini model. Defaults to 9.
        heads (int, optional): Number of attention heads. Defaults to 24.
        qk_norm (bool, optional): Whether to apply normalization to query and key. Defaults to True.
        ff_mult (int, optional): Multiplier for the feed-forward layer dimension. Defaults to 4.
        ring_seq_size (int, optional): Size of the ring sequence. Defaults to 512.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(
        self,
        dim: int,
        depth: int = 32,
        num_tokens: int = 10000,
        seq_len: int = 8192,
        dim_head: int = 128,
        long_gemini_depth: int = 9,
        heads: int = 24,
        qk_norm: bool = True,
        ff_mult: int = 4,
        ring_seq_size: int = 512,
        *args,
        **kwargs,
    ):
        super(LongGemini, self).__init__()
        self.dim = dim
        self.depth = depth
        self.num_tokens = num_tokens
        self.seq_len = seq_len
        self.dim_head = dim_head
        self.long_gemini_depth = long_gemini_depth
        self.heads = heads
        self.qk_norm = qk_norm
        self.ff_mult = ff_mult
        self.ring_seq_size = ring_seq_size

        self.output_head = OutputHead(
            dim,
            1,
        )

        # Layers for the model
        self.layers = nn.ModuleList(
            [
                LongGeminiTransformerBlock(
                    dim,
                    depth,
                    dim_head,
                    heads,
                    qk_norm,
                    ff_mult,
                    ring_seq_size,
                    *args,
                    **kwargs,
                )
                for _ in range(long_gemini_depth)
            ]
        )

        # Embedding layer for the model
        self.embed = nn.Embedding(num_tokens, dim)

    def forward(
        self, text: Tensor, audio: Tensor, img: Tensor, video: Tensor, *args, **kwargs
    ):
        """
        Forward pass of the LongGemini model.

        Args:
            x (Tensor): Input tensor.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Tensor: Output tensor.
        """
        # Text embedding
        x = self.embed(text)

        assert (
            (img is not None and audio is not None)
            or (img is not None and video is not None)
            or (audio is not None and video is not None)
        ), "At least two of the inputs (img, audio, video) must be provided."

        if img is not None:
            # Image dimensions
            img_b, img_c, img_h, img_w = img.shape

            # img = img_to_text(img, self.patches, self.patch_size, self.dim, True)
            img = img_to_text(img, self.max_seq_len, self.dim, True)

            if self.post_modal_transform_norm:
                img = self.pmt_norm(img)

        if audio is not None:
            # Audio dimensions
            audio_b, audio_seq_len = audio.shape

            audio = audio_to_text(audio, self.max_seq_len, self.dim, True)

            if self.post_modal_transform_norm:
                audio = self.pmt_norm(audio)

        if video is not None:
            # Video dimensions
            video_b, video_c, video_f, video_h, video_w = video.shape

            video = video_to_text(video, self.max_seq_len, self.dim, True)

        # Fuse layers
        if img is not None and audio is not None:
            torch.cat((img, audio), dim=1)
        elif img is not None and video is not None:
            torch.cat((img, video), dim=1)
        elif audio is not None and video is not None:
            torch.cat((audio, video), dim=1)

        # Apply the layers
        for layer in self.layers:
            x = layer(x)

        return self.output_head(x)


class Gemini(Module):
    """
    Gemini model implementation.

    Args:
    - num_tokens: Number of tokens in the input vocabulary (default: 50432)
    - max_seq_len: Maximum sequence length (default: 32052)
    - dim: Model dimension (default: 2560)
    - depth: Number of transformer layers (default: 32)
    - dim_head: Dimension of each attention head (default: 128)
    - heads: Number of attention heads (default: 24)
    - use_abs_pos_emb: Whether to use absolute positional embeddings (default: False)
    - attn_flash: Whether to use flash attention (default: True)
    - attn_kv_heads: Number of heads for key-value attention (default: 2)
    - qk_norm: Whether to apply layer normalization to query-key attention (default: True)
    - attn_qk_norm: Whether to apply layer normalization to query-key attention (default: True)
    - attn_qk_norm_dim_scale: Whether to scale the dimension of query-key attention layer normalization (default: True)
    - patches: Number of patches for image input (default: 16)
    - patch_size: Size of each patch for image input (default: 16)
    - img_channels: Number of channels in the image input (default: 3)
    - audio_seq_len: Length of audio sequence input (default: 128)
    - post_fusion_norm: Whether to apply layer normalization after fusion (default: True)
    - post_modal_transform_norm: Whether to apply layer normalization after modal transformation (default: False)
    - *args: Additional positional arguments
    - **kwargs: Additional keyword arguments
    """

    def __init__(
        self,
        num_tokens=50432,
        max_seq_len=32052,
        dim=2560,
        depth=32,
        dim_head=128,
        heads=24,
        use_abs_pos_emb=False,
        attn_flash=True,
        attn_kv_heads=2,
        qk_norm=True,
        attn_qk_norm=True,
        attn_qk_norm_dim_scale=True,
        patches: int = 16,
        patch_size: int = 16,
        img_channels: int = 3,
        audio_seq_len: int = 128,
        post_fusion_norm: bool = True,
        post_modal_transform_norm: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__()
        self.num_tokens = num_tokens
        self.max_seq_len = max_seq_len
        self.dim = dim
        self.depth = depth
        self.dim_head = dim_head
        self.heads = heads
        self.use_abs_pos_emb = use_abs_pos_emb
        self.attn_flash = attn_flash
        self.attn_kv_heads = attn_kv_heads
        self.qk_norm = qk_norm
        self.attn_qk_norm = attn_qk_norm
        self.attn_qk_norm_dim_scale = attn_qk_norm_dim_scale
        self.patches = patches
        self.patch_size = patch_size
        self.img_channels = img_channels
        self.audio_seq_len = audio_seq_len
        self.post_fusion_norm = post_fusion_norm
        self.post_modal_transform_norm = post_modal_transform_norm

        # Transformer model for the model
        self.gemini = Transformer(
            num_tokens=num_tokens,
            max_seq_len=max_seq_len,
            use_abs_pos_emb=use_abs_pos_emb,
            attn_layers=Decoder(
                dim=dim,
                depth=depth,
                dim_head=dim_head,
                heads=heads,
                attn_flash=attn_flash,
                attn_kv_heads=attn_kv_heads,
                qk_norm=qk_norm,
                attn_qk_norm=attn_qk_norm,
                attn_qk_norm_dim_scale=attn_qk_norm_dim_scale,
                cross_attend=True,
                *args,
                **kwargs,
            ),
        )

        # Autoregressive wrapper for the model
        self.decoder = AutoregressiveWrapper(self.gemini)

        # Post fusion norm
        if self.post_fusion_norm:
            self.psf_norm = nn.LayerNorm(dim)

        if self.post_modal_transform_norm:
            self.pmt_norm = nn.LayerNorm(dim)

    def forward(
        self,
        text: torch.Tensor = None,
        img: torch.Tensor = None,
        audio: torch.Tensor = None,
        video: torch.Tensor = None,
        *args,
        **kwargs,
    ):
        """
        Forward pass of the Gemini model.

        Args:
        - text: Text tensor
        - img: Image tensor
        - audio: Audio tensor
        - video: Video tensor
        - *args: Additional positional arguments
        - **kwargs: Additional keyword arguments

        Returns:
        - torch.Tensor: The output of the model

        Text input shape: [batch, seq_len, dim]
        img input shape: [batch, channels, height, width]
        audio input shape: [batch, audio_seq_len]
        video input shape: [batch, channels, frames, height, width]

        Output shape: [batch, seq_len, dim]
        """
        assert (
            (img is not None and audio is not None)
            or (img is not None and video is not None)
            or (audio is not None and video is not None)
        ), "At least two of the inputs (img, audio, video) must be provided."

        if img is not None:
            # Image dimensions
            img_b, img_c, img_h, img_w = img.shape

            # img = img_to_text(img, self.patches, self.patch_size, self.dim, True)
            img = img_to_text(img, self.max_seq_len, self.dim, True)

            if self.post_modal_transform_norm:
                img = self.pmt_norm(img)

        if audio is not None:
            # Audio dimensions
            audio_b, audio_seq_len = audio.shape

            audio = audio_to_text(audio, self.max_seq_len, self.dim, True)

            if self.post_modal_transform_norm:
                audio = self.pmt_norm(audio)

        if video is not None:
            # Video dimensions
            video_b, video_c, video_f, video_h, video_w = video.shape

            video = video_to_text(video, self.max_seq_len, self.dim, True)

        # Fuse layers
        if img is not None and audio is not None:
            fused = torch.cat((img, audio), dim=1)
        elif img is not None and video is not None:
            fused = torch.cat((img, video), dim=1)
        elif audio is not None and video is not None:
            fused = torch.cat((audio, video), dim=1)

        # Post fusion layernorm for stability.
        if self.post_fusion_norm:
            fused = self.psf_norm(fused)

        return self.decoder(text, context=fused, *args, **kwargs)
