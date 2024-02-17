import math
from typing import *
from warnings import warn

import torch
import torch.nn.functional as F
from einops import rearrange
from torch import einsum, nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer, LeakyReLU

from typing import Optional, Tuple, Union
from transformers.activations import ACT2FN

import sys, os
sys.path.insert(0, os.path.abspath("../models/"))
from .utils import *


# creating rotary positional embedding for giving a sequence to the data
def rotate_half(x: torch.Tensor) -> torch.Tensor:
    """
    The `rotate_half` method takes in a tensor `x` and rotates its last dimension by 180 degrees. The tensor is first
    rearranged to have a new dimension `j` which is equal to 2. The tensor is then split into two tensors `x1` and `x2`
    along the second to last dimension. The two tensors are then concatenated along the last dimension after the second
    tensor is negated. The resulting tensor has the same shape as the input tensor.

    :param x: input tensor
    :type x:
    :return: rotated tensor
    :rtype: torch.Tensor
    """

    x = rearrange(x, "... (j d) -> ... j d", j=2)
    x1, x2 = x.unbind(dim=-2)
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(pos: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
    """
    The `apply_rotary_pos_emb` method takes in two tensors `pos` and `t`. The `pos` tensor is a positional encoding
    tensor and `t` is the input tensor. The method applies a rotary positional encoding to the input tensor `t` using
    the positional encoding tensor `pos`. The method first applies a cosine function to the positional encoding tensor
    `pos` and element-wise multiplies it with the input tensor `t`. The method then applies a sine function to the
    positional encoding tensor `pos`, rotates it by 180 degrees using the `rotate_half` method, and element-wise
    multiplies it with the input tensor `t`. The two resulting tensors are then added together to produce the final
    output tensor.

    :param pos: positional encoding tensor
    :type pos: torch.Tensor
    :param t: input tensor
    :type t: torch.Tensor
    :return: final output tensor
    :rtype: torch.Tensor
    """

    return (t * pos.cos()) + (rotate_half(t) * pos.sin())


class TransformerHistory(nn.Module):

    def __init__(self, seq_num: int, seq_embed_dim: int = 100, seq_max_length: int = 8, seq_num_heads: int = 4,
                 seq_hidden_size: int = 512, seq_transformer_dropout: float = 0.0, seq_num_layers: int = 2,
                 seq_pooling_dropout: float = 0.0,
                 seq_pe: bool = True) -> None:

        """

        Initializes the TransformerHistory class with the given hyperparameters

        This class implements a Transformer-based model for time series forecasting. It takes in a sequence of inputs
        and outputs a single prediction. The model uses a TransformerEncoder to encode the input sequence and a
        MeanMaxPooling layer to aggregate the encoded sequence. The aggregated sequence is then passed through a linear
        layer to produce the final prediction. The architecture is based on the paper "Attention is all you need"
        - https://arxiv.org/abs/1706.03762

        .. highlight:: python
        .. code-block:: python

            import torch
            from torch import nn
            from vz_recommender.models.transformer import TransformerHistory

            model = TransformerHistory(seq_num=10, seq_embed_dim=32, seq_max_length=16, seq_num_heads=4, seq_hidden_size=64,
                seq_transformer_dropout=0.1, seq_num_layers=2, seq_pooling_dropout=0.2, seq_pe=True)
            input_seq = torch.randint(0, 10, (2, 16))
            valid_length = torch.tensor([8, 12])
            output = model(input_seq, valid_length)

        :param seq_num: number of unique values in the input sequence
        :type seq_num: int
        :param seq_embed_dim: dimensionality of the input sequence embeddings
        :type seq_embed_dim: int
        :param seq_max_length: maximum length of the input sequence
        :type seq_max_length: int
        :param seq_num_heads: number of attention heads in the TransformerEncoder
        :type seq_num_heads: int
        :param seq_hidden_size: size of the feedforward layer in the TransformerEncoder
        :type seq_hidden_size: int
        :param seq_transformer_dropout: dropout rate for the TransformerEncoder
        :type seq_transformer_dropout: float
        :param seq_num_layers: number of layers in the `TransformerEncoder`
        :type seq_num_layers: int
        :param seq_pooling_dropout: dropout rate for the `MeanMaxPooling` layer
        :type seq_pooling_dropout: float
        :param seq_pe: whether to use positional encoding for the input sequence
        :type seq_pe: bool
        """

        super().__init__()


        self.seq_embedding = nn.Embedding(seq_num, seq_embed_dim)
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    @staticmethod
    def create_key_padding_mask(seq_in: torch.Tensor, valid_length: torch.Tensor = None) -> torch.Tensor:

        """ Creates a key padding mask for the input sequence

        :param seq_in: input sequence tensor
        :type seq_in:
        :param valid_length: valid length of each sequence in the batch. If None, assumes all sequences are the same length
        :type valid_length:
        :return: tensor of shape (batch_size, seq_length) where 1 indicates a padded value and 0 indicates a valid value
        :rtype: torch.Tensor
        """

        device = seq_in.device
        vl_len = torch.cat((seq_in.size(0)*[torch.tensor([seq_in.size(1)])]), dim=0).to(device) if valid_length is None else valid_length
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(vl_len.unsqueeze(1))
        return mask

    def forward(self, seq_in: torch.Tensor, vl_in: torch.Tensor, seq_history=None):

        """
        Computes the forward pass of the TransformerHistory model

        :param seq_in: input sequence tensor of shape (batch_size, seq_length).
        :type seq_in: torch.Tensor
        :param vl_in: valid length of each sequence in the batch of shape (batch_size,).
        :type vl_in: torch.Tensor
        :param seq_history: historical sequence tensor of shape (batch_size, history_length, seq_length). Not used in
            this implementation.
        :type seq_history: torch.Tensor
        :return: A tensor of shape (batch_size, seq_embed_dim) representing the predicted value for each input sequence.
        :rtype:
        """

        seq_embed_out = self.seq_embedding(seq_in.long())
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)
        seq_out = self.seq_dense(seq_out)

        return seq_out


class TransformerAEP(TransformerHistory):
    """
    This class implements a Transformer-based model for session-based recommendation. It takes in page and item
    embeddings, and uses a TransformerEncoder to encode the sequence of user interactions. The encoded sequence is then
    passed through a MeanMaxPooling layer and a linear layer to generate the final recommendation. Please refer to the
    example below


    .. highlight:: python
    .. code-block:: python

        import torch
        from vz_recommender.models.transformer import TransformerHistory, TransformerAEP
        # initialize embeddings
        page_embedding = torch.nn.Embedding(num_embeddings=100, embedding_dim=32)
        item_embedding = torch.nn.Embedding(num_embeddings=1000, embedding_dim=64)
        # initialize TransformerAEP model
        model = TransformerAEP(page_embedding=page_embedding, item_embedding=item_embedding, seq_embed_dim=128)

        # generate recommendation
        page_in = torch.tensor([[1, 2, 3, 4, 5]])
        item_in = torch.tensor([[10, 20, 30, 40, 50]])
        vl_in = torch.tensor([5])
        seq_history = None
        recommendation = model(page_in=page_in, item_in=item_in, vl_in=vl_in, seq_history=seq_history)

    """
 
    def __init__(self, page_embedding: torch.nn.Embedding, item_embedding: torch.nn.Embedding, seq_embed_dim: int,
                 seq_max_length=8,
                 seq_num_heads=4, seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2,
                 seq_pooling_dropout=0.0, seq_pe=True) -> None:

        """
        Initializes the TransformerAEP model with the given hyperparameters.

        :param page_embedding: Embedding layer for pages
        :type page_embedding: torch.nn.Embedding
        :param item_embedding: Embedding layer for items
        :type item_embedding: torch.nn.Embedding
        :param seq_embed_dim: Dimension of the sequence embeddings
        :type seq_embed_dim: int
        :param seq_max_length: Maximum length of the sequence
        :type seq_max_length: int
        :param seq_num_heads: Number of attention heads in the `TransformerEncoder`
        :type seq_num_heads: int
        :param seq_hidden_size: Hidden size of the feedforward layer in the `TransformerEncoder`
        :type seq_hidden_size: int
        :param seq_transformer_dropout: Dropout probability for the `TransformerEncoder`
        :type seq_transformer_dropout: float
        :param seq_num_layers: Number of layers in the `TransformerEncoder`
        :type seq_num_layers: int
        :param seq_pooling_dropout: Dropout probability for the `MeanMaxPooling` layer
        :type seq_pooling_dropout: float
        :param seq_pe: Whether to use positional encoding in the `TransformerEncoder`
        :type seq_pe: bool
        """

        super().__init__(seq_embed_dim, seq_max_length=8, seq_num_heads=4, seq_hidden_size=512,
                         seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                         seq_pe=True)
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    def forward(self, page_in: torch.Tensor, item_in: torch.Tensor, vl_in: torch.Tensor,
                seq_history=None) -> torch.Tensor:

        """ Computes the forward pass of the TransformerAEP model.

        :param page_in: Input tensor of shape (batch_size, seq_length) containing page IDs
        :type page_in: torch.Tensor
        :param item_in: Input tensor of shape (batch_size, seq_length) containing item IDs
        :type item_in: torch.Tensor
        :param vl_in: Input tensor of shape (batch_size,) containing the valid length of each sequence
        :type vl_in: torch.Tensor
        :param seq_history: Not used in this implementation
        :type seq_history: None
        :return: Output tensor of shape (batch_size, seq_embed_dim) containing the recommendation for each sequence
        in the batch
        :rtype: torch.Tensor
        """

        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
        # seq_embed_out = torch.cat((page_embed_out, item_embed_out), 2)
        seq_embed_out = torch.mul(page_embed_out, item_embed_out)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=page_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)
        seq_out = self.seq_dense(seq_out)
        return seq_out


class ParallelTransformerBlock(nn.Module):
    """
    This class implements a PyTorch implementation of the ParallelTransformerBlock Transformer model. It includes
    methods for creating key padding masks, getting rotary embeddings, and forward propagation through the model.
    
    Instantiates Rotary Embedding ( RoPE https://arxiv.org/abs/2104.09864), Linear and SwiGLU Activation Layer (a
    variant of GLU https://arxiv.org/pdf/2002.05202.pdf). The architecture is based on the paper "PaLM: Scaling
    Language Modeling with Pathways" (https://arxiv.org/abs/2204.02311) The parallel formulation of transformer results
    in faster training speed at large scales

    .. highlight:: python
    .. code-block:: python

        import torch
        from vz_recommender.models.transformer import  ParallelTransformerBlock

        model = ParallelTransformerBlock(dim=512, dim_head=64, heads=8)
        input_data = torch.randn(10, 20, 512)
        output = model(input_data)
    """

    def __init__(self, dim, dim_head, heads, ff_mult=4, moe_kwargs=None) -> None:
        """
        Initializes the ParallelTransformerBlock model with the given parameters. Sets up the necessary layers and
        buffers for forward propagation. Shape O(1)

        :param dim: The dimension of the input data.
        :type dim: int
        :param dim_head: The dimension of the attention heads.
        :type dim_head: int
        :param heads: The number of attention heads.
        :type heads: int
        :param ff_mult: The multiplier for the feedforward layer.
        :type ff_mult: int
        :param moe_kwargs: Optional dictionary of arguments for the mixture of experts layer.
        :type moe_kwargs: dict
        """
        super().__init__()
        self.norm = LayerNorm(dim)

        attn_inner_dim = dim_head * heads
        ff_inner_dim = dim * ff_mult
        self.fused_dims = (attn_inner_dim, dim_head, dim_head, (ff_inner_dim * 2))

        self.heads = heads
        self.scale = dim_head**-0.5
        self.rotary_emb = RotaryEmbedding(dim_head)

        self.fused_attn_ff_proj = nn.Linear(dim, sum(self.fused_dims), bias=False)
        self.attn_out = nn.Linear(attn_inner_dim, dim, bias=False)
        
        self.ff_out = nn.Sequential(
            SwiGLU(),
            nn.Linear(ff_inner_dim, dim, bias=False)
        ) 
#         self.gate = Top2Gate(dim, moe_kwargs.get("num_experts"))
#         self.fused_attn_moe_proj = MOELayer(self.gate, self.fused_attn_ff_proj, sum(self.fused_dims))

        self.register_buffer("mask", None, persistent=False)
        self.register_buffer("pos_emb", None, persistent=False)
        
    @staticmethod
    def create_key_padding_mask(seq_in, valid_length=None):
        """
        Creates a key padding mask for the input sequence. Used to mask out padding tokens during attention
        calculations.  O(seq_length)

        :param seq_in: The input sequence tensor.
        :type seq_in: torch.Tensor
        :param valid_length: Optional tensor of valid lengths for each sequence in the batch.
        :type valid_length: torch.Tensor
        :return: A boolean mask tensor of shape (batch_size, seq_length).
        :rtype: torch.Tensor
        """
        device = seq_in.device
        vl_len = torch.cat((seq_in.size(0)*[torch.tensor([seq_in.size(1)])]), dim=0).to(device) if valid_length is None else valid_length
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(vl_len.unsqueeze(1))
        return mask

    def get_mask(self, n, device):
        """
        Gets a triangular mask for the attention calculation. Used to prevent attention from attending to future tokens.
        Method Shape - O(seq_length^2)

        :param n: The length of the sequence.
        :type n: int
        :param device: The device to create the mask on.
        :type device: torch.device
        :return: A boolean mask tensor of shape (seq_length, seq_length).
        :rtype: torch.Tensor

        """
        if self.mask is not None and self.mask.shape[-1] >= n:
            return self.mask[:n, :n]

        mask = torch.ones((n, n), device=device, dtype=torch.bool).triu(1)
        self.register_buffer("mask", mask, persistent=False)
        return mask

    def get_rotary_embedding(self, n, device):
        """
        Gets the rotary positional embedding for the input sequence. Method Shape: O(seq_length * dim_head)

        :param n: The length of the sequence.
        :type n: int
        :param device: The device to create the embedding on.
        :type device: torch.device
        :return: A tensor of shape (seq_length, dim_head).
        :rtype: torch.Tensor
        """

        if self.pos_emb is not None and self.pos_emb.shape[-2] >= n:
            return self.pos_emb[:n]

        pos_emb = self.rotary_emb(n, device=device)
        self.register_buffer("pos_emb", pos_emb, persistent=False)
        return pos_emb

    def forward(self, x, vl=None):
        """
        Performs forward propagation through the ParallelTransformerBlock model. Method Shape: O(seq_length^2 * dim)

        :param x: The input sequence tensor of shape (batch_size, seq_length, dim).
        :type x: torch.Tensor
        :param vl: Optional tensor of valid lengths for each sequence in the batch.
        :type vl: torch.Tensor
        :return: The output tensor of shape (batch_size, seq_length, dim).
        :rtype: torch.Tensor

        """

        n, device, h = x.shape[1], x.device, self.heads
        x = self.norm(x)
        # attention queries, keys, values, and feedforward inner
        #creates attention heads 
        #shape of q : [batch size, 2*vl]
        #shape of k : [batch_size, 2*vl]
        #shape of ff : [batch_size, 8*vl]
#         x, aux_loss = self.fused_attn_moe_proj(x)
        x = self.fused_attn_ff_proj(x)
        q, k, v, ff = x.split(self.fused_dims, dim=-1)
        q = rearrange(q, "b n (h d) -> b h n d", h=h)

        positions = self.get_rotary_embedding(n, device)
        q, k = map(lambda t: apply_rotary_pos_emb(positions, t), (q, k))
        q = q * self.scale
        sim = einsum("b h i d, b j d -> b h i j", q, k)

#         causal_mask = self.get_mask(n, device)
        mask = self.create_key_padding_mask(seq_in=x, valid_length=vl)
        sim = sim.masked_fill(mask.unsqueeze(1).unsqueeze(2), float('-inf'))

        attn = sim.softmax(dim=-1)

        out = einsum("b h i j, b j d -> b h i d", attn, v)

        out = rearrange(out, "b h n d -> b n (h d)")
#         out, aux_loss = self.fused_attn_moe_proj(out)

        out = self.attn_out(out) + self.ff_out(ff)
        return out
    

class ParallelTransformerAEP(nn.Module):
    """
    This class implements a Parallel Transformer Autoencoder with Page-Item Attention for recommendation systems. It
    takes in page and item embeddings, along with various meta data, and applies a parallel transformer block to encode
    the data and generate a recommendation.

    .. highlight:: python
    .. code-block:: python

        import sys
        import torch
        from torch import nn
        from vz_recommender.models.transformer import ParallelTransformerAEP

        model = ParallelTransformerAEP(page_embedding, item_embedding, dim=512, dim_head=64, heads=8, num_layers=6,
            num_page_meta_wide=0, page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0,
            ff_mult=4, seq_pooling_dropout=0.0, page_meta_embedding=None, item_meta_embedding=None,
            item_pre_embedding=None, moe_kwargs=None)
        output = model(page_in, item_in, item_meta_in, vl_in, page_meta_in=None, page_meta_wide_in=None,
            item_meta_wide_in=None)
    """
 
    def __init__(self, page_embedding, item_embedding, dim, dim_head, heads, num_layers, num_page_meta_wide=0,
                 page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0, ff_mult=4,
                 seq_pooling_dropout=0.0, page_meta_embedding=None, item_meta_embedding=None, item_pre_embedding=None,
                 moe_kwargs=None) -> None:

        """
        Initializes the ParallelTransformerAEP class with the given parameters.

        :param page_embedding: Embedding for pages
        :type page_embedding: torch.nn.Embedding
        :param item_embedding: Embedding for items
        :type item_embedding: torch.nn.Embedding
        :param dim: Dimension of the model
        :type dim: int
        :param dim_head: Dimension of the attention head
        :type dim_head: int
        :param heads: Number of attention heads
        :type heads: int
        :param num_layers: number of transformer layers
        :type num_layers: int
        :param num_page_meta_wide: Number of wide meta data for pages
        :type num_page_meta_wide: int
        :param page_meta_wide_embed_dim: Embedding dimension for wide meta data for pages
        :type page_meta_wide_embed_dim: int
        :param num_item_meta_wide: Number of wide meta data for items
        :type num_item_meta_wide: int
        :param item_meta_wide_embed_dim: Embedding dimension for wide meta data for items
        :type item_meta_wide_embed_dim: int
        :param ff_mult:  Multiplier for feedforward network
        :type ff_mult: int
        :param seq_pooling_dropout: Dropout rate for sequence pooling
        :type seq_pooling_dropout: float
        :param page_meta_embedding: Embedding for page metadata
        :type page_meta_embedding: torch.nn.Embedding
        :param item_meta_embedding: Embedding for item metadata
        :type item_meta_embedding: torch.nn.Embedding
        :param item_pre_embedding: Embedding for item pre data
        :type item_pre_embedding: torch.nn.Embedding
        :param moe_kwargs: Dictionary of arguments for mixture of experts
        :type moe_kwargs: dict
        """

        super().__init__()
        self.page_embedding = page_embedding
        self.page_meta_embedding = page_meta_embedding
        if num_page_meta_wide > 0:
            self.num_page_meta_wide = num_page_meta_wide
            self.page_meta_wide_dense = nn.Linear(num_page_meta_wide, page_meta_wide_embed_dim)
            self.page_meta_wide_act = nn.LeakyReLU(0.2)
        if num_page_meta_wide > 1:
            self.page_meta_wide_batch_norm = nn.BatchNorm1d(num_page_meta_wide)
        self.item_embedding = item_embedding
        self.item_meta_embedding = item_meta_embedding
        self.item_pre_embedding = item_pre_embedding
        if num_item_meta_wide > 0:
            self.num_item_meta_wide = num_item_meta_wide
            self.item_meta_wide_dense = nn.Linear(num_item_meta_wide, item_meta_wide_embed_dim)
            self.item_meta_wide_act = nn.LeakyReLU(0.2)
        if num_item_meta_wide > 1:
            self.item_meta_wide_batch_norm = nn.BatchNorm1d(num_item_meta_wide)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)  
        self.num_layers = num_layers
        
        # use parallel transformer. pls comment if want to test simplified transformer.
        self.ptransformer = nn.ModuleList([
            Residual(ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult, moe_kwargs=moe_kwargs))
            for _ in range(self.num_layers)
        ])

        # # uncomment this part for testing simplified transformer block
        # self.ptransformer = nn.ModuleList([
        #     SimplifiedTransformerBlock(dim=dim, heads=heads, n_layer=self.num_layers, ff_mult=ff_mult, layer_idx=i)
        #     for i in range(self.num_layers)
        # ])


    def forward(self, page_in, item_in, item_meta_in, vl_in, page_meta_in=None, page_meta_wide_in=None, item_meta_wide_in=None):
        """
        Applies the forward pass of the ParallelTransformerAEP model to the given input data.

        :param page_in: Input tensor for pages
        :type page_in: torch.Tensor
        :param item_in: Input tensor for items
        :type item_in: torch.Tensor
        :param item_meta_in: Input tensor for item meta data
        :type item_meta_in: torch.Tensor
        :param vl_in: Input tensor for visual and language data
        :type vl_in: torch.Tensor
        :param page_meta_in:  Input tensor for page meta data
        :type page_meta_in: torch.Tensor
        :param page_meta_wide_in: List of input tensors for wide page meta data
        :type page_meta_wide_in: List[torch.Tensor]
        :param item_meta_wide_in: List of input tensors for wide item meta data
        :type item_meta_wide_in: List[torch.Tensor]
        :return: Output tensor (batch_size, dim) of the `ParallelTransformerAEP` model
        :rtype: torch.Tensor
        """

        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())

        if page_meta_in is not None:
            page_meta_embed_out = self.page_meta_embedding(page_meta_in.long())
        if item_meta_in is not None:
            item_meta_embed_out = self.item_meta_embedding(item_meta_in.long())
            item_pre_embed_out = self.item_pre_embedding(item_in.long())

        if page_meta_wide_in is not None:
            page_meta_wide_in_list = [wide_i.float() for wide_i in page_meta_wide_in]
            page_meta_wide_cat = torch.stack(page_meta_wide_in_list, dim=0)
            if self.num_page_meta_wide > 1:
                page_meta_wide_out_norm = self.page_meta_wide_batch_norm(page_meta_wide_cat)
            else:
                page_meta_wide_out_norm = page_meta_wide_cat
            page_meta_wide_out_norm = torch.permute(page_meta_wide_out_norm, (0, 2, 1))
            page_meta_wide_out_norm = self.page_meta_wide_dense(page_meta_wide_out_norm)
            page_meta_wide_out_norm = self.page_meta_wide_act(page_meta_wide_out_norm)
            if page_meta_in is not None:
                page_full_out = torch.cat((page_embed_out, page_meta_embed_out, page_meta_wide_out_norm), 2)
            else:
                page_full_out = torch.cat((page_embed_out, page_meta_wide_out_norm), 2)
        else:
            if page_meta_in is not None:
                page_full_out = torch.cat((page_embed_out, page_meta_embed_out), 2)
            else:
                page_full_out = page_embed_out

        if item_meta_wide_in is not None:
            item_meta_wide_in_list = [wide_i.float() for wide_i in item_meta_wide_in]
            item_meta_wide_cat = torch.stack(item_meta_wide_in_list, dim=0)
            if self.num_item_meta_wide > 1:
                item_meta_wide_out_norm = self.item_meta_wide_batch_norm(item_meta_wide_cat)
            else:
                item_meta_wide_out_norm = item_meta_wide_cat
            item_meta_wide_out_norm = torch.permute(item_meta_wide_out_norm, (0, 2, 1))
            item_meta_wide_out_norm = self.item_meta_wide_dense(item_meta_wide_out_norm)
            item_meta_wide_out_norm = self.item_meta_wide_act(item_meta_wide_out_norm)
            if item_meta_in is not None:
                item_full_out = torch.cat(
                    (item_embed_out, item_meta_embed_out, item_pre_embed_out, item_meta_wide_out_norm), 2)
            else:
                item_full_out = torch.cat((item_embed_out, item_meta_wide_out_norm), 2)
        else:
            if item_meta_in is not None:
                item_full_out = torch.cat((item_embed_out, item_meta_embed_out, item_pre_embed_out), 2)
            else:
                item_full_out = item_embed_out

        x = torch.mul(page_full_out, item_full_out)
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, vl_in)

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)
        return out


class SimplifiedTransformerAEP(nn.Module):
    """
    This class implements a Parallel Transformer Autoencoder with Page-Item Attention for recommendation systems. It takes in page and item embeddings, along with various meta data, and applies a parallel transformer block to encode the data and generate a recommendation.

    ## Class Example -
    import torch
    from torch import nn
    from vz_recommender.models.transformer import ParallelTransformerAEP

    model = ParallelTransformerAEP(page_embedding, item_embedding, dim=512, dim_head=64, heads=8, num_layers=6, num_page_meta_wide=0, page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0, ff_mult=4, seq_pooling_dropout=0.0, page_meta_embedding=None, item_meta_embedding=None, item_pre_embedding=None, moe_kwargs=None)
    output = model(page_in, item_in, item_meta_in, vl_in, page_meta_in=None, page_meta_wide_in=None, item_meta_wide_in=None)
    """

    def __init__(self, page_embedding, item_embedding, dim, dim_head, heads, num_layers, num_page_meta_wide=0,
                 page_meta_wide_embed_dim=0, num_item_meta_wide=0, item_meta_wide_embed_dim=0, ff_mult=4,
                 seq_pooling_dropout=0.0, page_meta_embedding=None, item_meta_embedding=None, item_pre_embedding=None,
                 moe_kwargs=None):
        """
        ## Method - __init__()
        ## Method Comment - Initializes the ParallelTransformerAEP class with the given parameters.
        ## Method Arguments -
        - page_embedding: torch.nn.Embedding - Embedding for pages
        - item_embedding: torch.nn.Embedding - Embedding for items
        - dim: int - Dimension of the model
        - dim_head: int - Dimension of the attention head
        - heads: int - Number of attention heads
        - num_layers: int - Number of transformer layers
        - num_page_meta_wide: int - Number of wide meta data for pages
        - page_meta_wide_embed_dim: int - Embedding dimension for wide meta data for pages
        - num_item_meta_wide: int - Number of wide meta data for items
        - item_meta_wide_embed_dim: int - Embedding dimension for wide meta data for items
        - ff_mult: int - Multiplier for feedforward network
        - seq_pooling_dropout: float - Dropout rate for sequence pooling
        - page_meta_embedding: torch.nn.Embedding - Embedding for page meta data
        - item_meta_embedding: torch.nn.Embedding - Embedding for item meta data
        - item_pre_embedding: torch.nn.Embedding - Embedding for item pre data
        - moe_kwargs: dict - Dictionary of arguments for mixture of experts
        ## Method Return - None
        ## Method Shape - N/A
        """
        super().__init__()
        self.page_embedding = page_embedding
        self.page_meta_embedding = page_meta_embedding
        if num_page_meta_wide > 0:
            self.num_page_meta_wide = num_page_meta_wide
            self.page_meta_wide_dense = nn.Linear(num_page_meta_wide, page_meta_wide_embed_dim)
            self.page_meta_wide_act = nn.LeakyReLU(0.2)
        if num_page_meta_wide > 1:
            self.page_meta_wide_batch_norm = nn.BatchNorm1d(num_page_meta_wide)
        self.item_embedding = item_embedding
        self.item_meta_embedding = item_meta_embedding
        self.item_pre_embedding = item_pre_embedding
        if num_item_meta_wide > 0:
            self.num_item_meta_wide = num_item_meta_wide
            self.item_meta_wide_dense = nn.Linear(num_item_meta_wide, item_meta_wide_embed_dim)
            self.item_meta_wide_act = nn.LeakyReLU(0.2)
        if num_item_meta_wide > 1:
            self.item_meta_wide_batch_norm = nn.BatchNorm1d(num_item_meta_wide)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)
        self.num_layers = num_layers

        self.ptransformer = nn.ModuleList([
            SimplifiedTransformerBlock(hidden_size=dim, heads=heads, ff_mult=ff_mult, n_layer=self.num_layers,
                                       layer_idx=i)
            for i in range(self.num_layers)
        ])

    def forward(self, page_in, item_in, item_meta_in, vl_in, page_meta_in=None, page_meta_wide_in=None,
                item_meta_wide_in=None):
        """
        ## Method - forward()
        ## Method Comment - Applies the forward pass of the ParallelTransformerAEP model to the given input data.
        ## Method Arguments -
        - page_in: torch.Tensor - Input tensor for pages
        - item_in: torch.Tensor - Input tensor for items
        - item_meta_in: torch.Tensor - Input tensor for item meta data
        - vl_in: torch.Tensor - Input tensor for visual and language data
        - page_meta_in: torch.Tensor - Input tensor for page meta data
        - page_meta_wide_in: List[torch.Tensor] - List of input tensors for wide page meta data
        - item_meta_wide_in: List[torch.Tensor] - List of input tensors for wide item meta data
        ## Method Return - torch.Tensor - Output tensor of the ParallelTransformerAEP model
        ## Method Shape - (batch_size, dim)
        """
        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())

        if page_meta_in is not None:
            page_meta_embed_out = self.page_meta_embedding(page_meta_in.long())
        if item_meta_in is not None:
            item_meta_embed_out = self.item_meta_embedding(item_meta_in.long())
            item_pre_embed_out = self.item_pre_embedding(item_in.long())

        if page_meta_wide_in is not None:
            page_meta_wide_in_list = [wide_i.float() for wide_i in page_meta_wide_in]
            page_meta_wide_cat = torch.stack(page_meta_wide_in_list, dim=0)
            if self.num_page_meta_wide > 1:
                page_meta_wide_out_norm = self.page_meta_wide_batch_norm(page_meta_wide_cat)
            else:
                page_meta_wide_out_norm = page_meta_wide_cat
            page_meta_wide_out_norm = torch.permute(page_meta_wide_out_norm, (0, 2, 1))
            page_meta_wide_out_norm = self.page_meta_wide_dense(page_meta_wide_out_norm)
            page_meta_wide_out_norm = self.page_meta_wide_act(page_meta_wide_out_norm)
            if page_meta_in is not None:
                page_full_out = torch.cat((page_embed_out, page_meta_embed_out, page_meta_wide_out_norm), 2)
            else:
                page_full_out = torch.cat((page_embed_out, page_meta_wide_out_norm), 2)
        else:
            if page_meta_in is not None:
                page_full_out = torch.cat((page_embed_out, page_meta_embed_out), 2)
            else:
                page_full_out = page_embed_out

        if item_meta_wide_in is not None:
            item_meta_wide_in_list = [wide_i.float() for wide_i in item_meta_wide_in]
            item_meta_wide_cat = torch.stack(item_meta_wide_in_list, dim=0)
            if self.num_item_meta_wide > 1:
                item_meta_wide_out_norm = self.item_meta_wide_batch_norm(item_meta_wide_cat)
            else:
                item_meta_wide_out_norm = item_meta_wide_cat
            item_meta_wide_out_norm = torch.permute(item_meta_wide_out_norm, (0, 2, 1))
            item_meta_wide_out_norm = self.item_meta_wide_dense(item_meta_wide_out_norm)
            item_meta_wide_out_norm = self.item_meta_wide_act(item_meta_wide_out_norm)
            if item_meta_in is not None:
                item_full_out = torch.cat(
                    (item_embed_out, item_meta_embed_out, item_pre_embed_out, item_meta_wide_out_norm), 2)
            else:
                item_full_out = torch.cat((item_embed_out, item_meta_wide_out_norm), 2)
        else:
            if item_meta_in is not None:
                item_full_out = torch.cat((item_embed_out, item_meta_embed_out, item_pre_embed_out), 2)
            else:
                item_full_out = item_embed_out

        x = torch.mul(page_full_out, item_full_out)
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, vl_in)

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)
        return out



class ParallelTransformerAEP2S(nn.Module):

    """
    This class implements a parallel transformer model for recommendation systems. It takes page and item embeddings,
    applies transformer blocks to them, and returns a sequence-pooled output.

    .. highlight:: python
    .. code-block:: python

        # Instantiate the class with appropriate parameters and call the forward method with page, item, and vl inputs
        to get the output.
        import torch
        from torch import nn
        from vz_recommender.models.transformer import ParallelTransformerAEP2S

        num_pages = 4
        embedding_dim = 32
        num_items = 6

        page_embedding = nn.Embedding(num_pages, embedding_dim)
        item_embedding = nn.Embedding(num_items, embedding_dim)
        model = ParallelTransformerAEP2S(page_embedding, item_embedding, dim=512, dim_head=64, heads=8, num_layers=6)
    """

    warn("this class is a simplified duplicate...Use ParallelTransformerAEP instead", DeprecationWarning, stacklevel=2)

    def __init__(self, page_embedding, item_embedding, dim, dim_head, heads, num_layers, ff_mult=4,
                 seq_pooling_dropout=0.0, moe_kwargs=None) -> None:
        """
        This method initializes the ParallelTransformerAEP2S class with the given parameters.

        :param page_embedding: Embedding matrix for pages
        :type page_embedding:
        :param item_embedding: Embedding matrix for items
        :type item_embedding:
        :param dim: Dimension of the embeddings
        :type dim:
        :param dim_head: Dimension of each head in the multi-head attention
        :type dim_head:
        :param heads: Number of heads in the multi-head attention
        :type heads: int
        :param num_layers: Number of transformer layers
        :type num_layers: int
        :param ff_mult: Multiplier for the feedforward layer dimension
        :type ff_mult:
        :param seq_pooling_dropout: Dropout probability for the sequence pooling layer
        :type seq_pooling_dropout: float
        :param moe_kwargs: Keyword arguments for the mixture-of-experts layer
        :type moe_kwargs:
        """
        super().__init__()

        warn('Class ParallelTransformerAEP2S is deprecated, use Class ParallelTransformerAEP instead', stacklevel=2)
        
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)
        self.num_layers = num_layers
        #         self.ptransformer = nn.ModuleList([
        #             ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult, moe_kwargs=moe_kwargs)
        #             for _ in range(self.num_layers)
        #         ])

        self.ptransformer = nn.ModuleList([
            Residual(ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult,
                                              moe_kwargs=moe_kwargs))
            for _ in range(self.num_layers)
        ])

    def forward(self, page_in, item_in, vl_in):
        """
        This method takes page, item, and vl inputs, applies transformer blocks to them, and returns a sequence-pooled
        output.

        :param page_in: Input tensor of page indices (batch_size, seq_len)
        :type page_in: torch.Tensor
        :param item_in: Input tensor of item indices (batch_size, seq_len)
        :type item_in: torch.Tensor
        :param vl_in: Input tensor of visual features (batch_size, seq_len, vl_dim)
        :type vl_in: torch.Tensor
        :return: Output tensor after applying transformer blocks and sequence pooling (batch_size, dim)
        :rtype: torch.Tensor
        """

        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
        #         aux_loss = 0
        x = torch.mul(page_embed_out, item_embed_out)
        #         x = torch.cat((page_embed_out, item_embed_out), 2)
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, vl_in)
        #             x, aux_loss = self.ptransformer[i](x, vl_in)
        #             aux_loss += aux_loss

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)
        return out


class ParallelTransformerIHQ(nn.Module):
    """
    This class implements a parallel transformer model for recommendation systems. It takes page and item embeddings, applies transformer blocks to them, and returns a sequence-pooled output.

    ## Class Example - Instantiate the class with appropriate parameters and call the forward method with page, item, and vl inputs to get the output.
    import torch
    from torch import nn
    from vz_recommender.models.transformer import ParallelTransformerAEP2S

    num_pages = 4
    embedding_dim = 32
    num_items = 6

    ihq_embedding = nn.Embedding(num_ihq, embedding_dim)
    model = ParallelTransformerAEP2S(page_embedding, item_embedding, dim=512, dim_head=64, heads=8, num_layers=6)
    """

    def __init__(self, ihq_embedding, dim, dim_head, heads, num_layers, ihq_pooling_dropout=0.0, ff_mult=4):
        """
        ## Method - __init__()
        ## Method Comment - This method initializes the ParallelTransformerAEP2S class with the given parameters.
        ## Method Arguments -
            - ihq_embedding: Embedding matrix for ihq
            - dim: Dimension of the embeddings
            - dim_head: Dimension of each head in the multi-head attention
            - heads: Number of heads in the multi-head attention
            - num_layers: Number of transformer layers
            - ff_mult: Multiplier for the feedforward layer dimension
            - seq_pooling_dropout: Dropout probability for the sequence pooling layer
            - moe_kwargs: Keyword arguments for the mixture-of-experts layer
        ## Method Return - None
        ## Method Shape - None
        """
        super().__init__()
        self.ihq_embedding = ihq_embedding
        self.num_layers = num_layers
        self.seq_pooling_dp = MeanMaxPooling(dropout=ihq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)
        self.ptransformer = nn.ModuleList([
            Residual(ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult))
            for _ in range(self.num_layers)
        ])

    def forward(self, ihq_in, ihq_vl_in):
        """
        ## Method - forward()
        ## Method Comment - This method takes page, item, and vl inputs, applies transformer blocks to them, and returns a sequence-pooled output.
        ## Method Arguments -
            - page_in: Input tensor of page indices
            - item_in: Input tensor of item indices
            - vl_in: Input tensor of visual features
        ## Method Return - Output tensor after applying transformer blocks and sequence pooling
        ## Method Shape - Input: (batch_size, seq_len), (batch_size, seq_len), (batch_size, seq_len, vl_dim) | Output: (batch_size, dim)
        """

        x = self.ihq_embedding(ihq_in.long())
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, ihq_vl_in)

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)

        return out


class ParallelTransformerSingleSeq(nn.Module):
    def __init__(self, seq_dim, dim, dim_head, heads, num_layers, seq_pooling_dropout=0.0, ff_mult=4):
        super().__init__()
        self.seq_embedding = nn.Embedding(seq_dim, dim)
        self.num_layers = num_layers
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)
        self.ptransformer = nn.ModuleList([
            Residual(ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult))
            for _ in range(self.num_layers)
        ])

    def forward(self, seq_in, seq_vl_in):
        x = self.seq_embedding(seq_in.long())
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, seq_vl_in)

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)

        return out



class ParallelTransformerMultiSeq(nn.Module):
    def __init__(self, seq_dims, dim, dim_head, heads, num_layers, seq_pooling_dropout=0.0, ff_mult=4):
        super().__init__()
        self.seq_transformers = nn.ModuleList([
            ParallelTransformerSingleSeq(seq_dim, dim, dim_head, heads, num_layers, seq_pooling_dropout, ff_mult)
            for seq_dim in seq_dims
        ])
        self.num_layers = num_layers
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)

    def forward(self, multi_seq_in, multi_seq_vl_in):
        outs = []
        for i in range(len(multi_seq_vl_in)):
            x = self.seq_transformers[i](multi_seq_in[i], multi_seq_vl_in[i])
            outs.append(x)

        out = torch.stack(outs, axis=1)
        out = self.seq_pooling_dp(out)
        out = self.seq_dense(out)

        return out


class SimplifiedTransformerBlock(nn.Module):

    """
    A customisable GPT2Block that implements Pre-LN, parallel, and skipless blocks. The architecture is based on
    paper: Simplifying Transformer Blocks (https://arxiv.org/abs/2311.01906) github of the implementation for
    reference: https://github.com/bobby-he/simplified_transformers

    .. highlight:: python
    .. code-block:: python

        import torch
        from vz_recommender.models.transformer import  SimplifiedTransformerBlock

    model = SimplifiedTransformerBlock(dim=256, heads=8, layer_idx=None)
    input_data = torch.randn(32, 128, 256) # input tensor shape: (batch_size, seq_length, dim)
        output = model(input_data)
    """
    def __init__(self, dim, ff_mult=4,
                 n_layer=12,
                 heads=8,
                 scale_attn_weights=False,
                 scale_attn_by_inverse_layer_idx=False,
                 first_layer_value_resid_gain=1,
                 value_resid_gain=0,
                 value_skip_gain=1,
                 val_init_type="id",
                 trainable_value_gains=True,
                 trainable_proj_gains=True,
                 last_layer_proj_resid_gain=None,
                 proj_resid_gain=0,
                 proj_skip_gain=1,
                 proj_init_type="id",
                 query_init_std=0,
                 key_init_std=None,
                 val_proj_init_std=None,
                 attn_mat_resid_gain=1,
                 trainable_attn_mat_gains=True,
                 attn_mat_skip_gain=1,
                 centre_attn=True,
                 centre_attn_gain=1,
                 attn_pdrop=0.1,
                 resid_pdrop=0.1,
                 parallel_layers=True, 
                 norm_type="none", 
                 layer_norm_epsilon=1e-08, 
                 norm_position='pre', 
                 attn_block_resid_gain=1,
                 trainable_attn_block_gains=True, 
                 attn_block_skip_gain=0,  
                 mlp_block_resid_gain=0.1, 
                 trainable_mlp_block_gains=True, 
                 mlp_block_skip_gain=0, 
                 activation_function="leaky_relu",
                 lrelu_neg_slope=0, 
                 mlp_proj_init_std=None,
                 decoder_only=False,
                 layer_idx=None):

        """

        :param hidden_size:
        :type hidden_size: int
        :param ff_mult:
        :type ff_mult: int
        :param max_position_embeddings:
        :type max_position_embeddings: int
        :param n_layer:
        :type n_layer: int
        :param num_attention_heads:
        :type num_attention_heads: int
        :param scale_attn_weights:
        :type scale_attn_weights:
        :param scale_attn_by_inverse_layer_idx:
        :type scale_attn_by_inverse_layer_idx: bool
        :param first_layer_value_resid_gain:
        :type first_layer_value_resid_gain: int
        :param value_resid_gain:
        :type value_resid_gain:
        :param value_skip_gain:
        :type value_skip_gain:
        :param val_init_type:
        :type val_init_type:
        :param trainable_value_gains:
        :type trainable_value_gains:
        :param trainable_proj_gains:
        :type trainable_proj_gains:
        :param last_layer_proj_resid_gain:
        :type last_layer_proj_resid_gain:
        :param proj_resid_gain:
        :type proj_resid_gain:
        :param proj_skip_gain:
        :type proj_skip_gain:
        :param proj_init_type:
        :type proj_init_type:
        :param query_init_std:
        :type query_init_std:
        :param key_init_std:
        :type key_init_std:
        :param val_proj_init_std:
        :type val_proj_init_std:
        :param attn_mat_resid_gain:
        :type attn_mat_resid_gain:
        :param trainable_attn_mat_gains:
        :type trainable_attn_mat_gains:
        :param attn_mat_skip_gain:
        :type attn_mat_skip_gain:
        :param centre_attn:
        :type centre_attn:
        :param centre_attn_gain:
        :type centre_attn_gain:
        :param attn_pdrop:
        :type attn_pdrop:
        :param resid_pdrop:
        :type resid_pdrop:
        :param parallel_layers:
        :type parallel_layers:
        :param norm_type:
        :type norm_type:
        :param layer_norm_epsilon:
        :type layer_norm_epsilon:
        :param norm_position:
        :type norm_position:
        :param attn_block_resid_gain:
        :type attn_block_resid_gain:
        :param trainable_attn_block_gains:
        :type trainable_attn_block_gains:
        :param attn_block_skip_gain:
        :type attn_block_skip_gain:
        :param mlp_block_resid_gain:
        :type mlp_block_resid_gain:
        :param trainable_mlp_block_gains:
        :type trainable_mlp_block_gains:
        :param mlp_block_skip_gain:
        :type mlp_block_skip_gain:
        :param activation_function:
        :type activation_function:
        :param lrelu_neg_slope:
        :type lrelu_neg_slope:
        :param mlp_proj_init_std:
        :type mlp_proj_init_std:
        :param decoder_only:
        :type decoder_only:
        :param layer_idx:
        :type layer_idx:
        """


        super().__init__()
        self.parallel_layers = parallel_layers
        self.layer_idx = layer_idx

        if norm_type == "ln":
            self.ln_1 = nn.LayerNorm(dim, eps=layer_norm_epsilon)
            self.ln_2 = nn.LayerNorm(dim, eps=layer_norm_epsilon)
        elif norm_type == "rmsnorm":
            self.ln_1 = RMSNorm(dim, eps=layer_norm_epsilon)
            self.ln_2 = RMSNorm(dim, eps=layer_norm_epsilon)
        elif norm_type == "none":
            # always use LN in first layer to normalise input activation norms.
            self.ln_1 = (
                nn.Identity()
                if (layer_idx is not None and layer_idx > 0) or layer_idx is None
                else nn.LayerNorm(dim, eps=layer_norm_epsilon)
            )
            self.ln_2 = nn.Identity()
        else:
            raise NotImplementedError

        self.norm_position = norm_position

        self.attn = SimplifiedAttention(
                 dim=dim,
                 n_layer=n_layer,
                 heads=heads,
                 scale_attn_weights=scale_attn_weights,
                 scale_attn_by_inverse_layer_idx=scale_attn_by_inverse_layer_idx,
                 first_layer_value_resid_gain=first_layer_value_resid_gain,
                 value_resid_gain=value_resid_gain,
                 value_skip_gain=value_skip_gain,
                 val_init_type=val_init_type,
                 trainable_value_gains=trainable_value_gains,
                 trainable_proj_gains=trainable_proj_gains,
                 last_layer_proj_resid_gain=last_layer_proj_resid_gain,
                 proj_resid_gain=proj_resid_gain,
                 proj_skip_gain=proj_skip_gain,
                 proj_init_type=proj_init_type,
                 query_init_std=query_init_std,
                 key_init_std=key_init_std,
                 val_proj_init_std=val_proj_init_std,
                 attn_mat_resid_gain=attn_mat_resid_gain,
                 trainable_attn_mat_gains=trainable_attn_mat_gains,
                 attn_mat_skip_gain=attn_mat_skip_gain,
                 centre_attn=centre_attn,
                 centre_attn_gain=centre_attn_gain,
                 attn_pdrop=attn_pdrop,
                 resid_pdrop=resid_pdrop,
                 decoder_only=decoder_only,
                 layer_idx=layer_idx)

        self.mlp = SimplifiedMLP(ff_mult, dim, activation_function,
                 lrelu_neg_slope, resid_pdrop, mlp_proj_init_std)
        self.attn_block_resid_gain = nn.Parameter(
            torch.Tensor([attn_block_resid_gain]),
            requires_grad=trainable_attn_block_gains,
        )
        self.attn_block_skip_gain = nn.Parameter(
            torch.Tensor([attn_block_skip_gain]),
            requires_grad=trainable_attn_block_gains
            and not self.parallel_layers,
        )
        self.mlp_block_resid_gain = nn.Parameter(
            torch.Tensor([mlp_block_resid_gain]),
            requires_grad=trainable_mlp_block_gains,
        )
        self.mlp_block_skip_gain = nn.Parameter(
            torch.Tensor([mlp_block_skip_gain]),
            requires_grad=trainable_mlp_block_gains and not self.parallel_layers,
        )
        self.add_attn_skip = attn_block_skip_gain != 0
        self.add_mlp_skip = mlp_block_skip_gain != 0

    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        vl: Optional[torch.Tensor] = None
    ) -> torch.Tensor:

        """

        :param hidden_states:
        :type hidden_states: Optional[Tuple[torch.FloatTensor]]
        :param layer_past:
        :type layer_past: Optional[Tuple[torch.Tensor]]
        :param vl:
        :type vl:
        :param output_attentions:
        :type output_attentions:
        :return:
        :rtype:
        """

        if self.norm_position == "post":
            hidden_states = self.ln_1(hidden_states)
        skip_branch = hidden_states
        if self.norm_position == "pre":
            hidden_states = self.ln_1(hidden_states)

        attn_outputs = self.attn(
            hidden_states,
            val_len=vl
        )
        attn_output = attn_outputs[0]  # output_attn: a, present, (attentions)

        if self.parallel_layers:
            # Parallel block of GPT-J
            feed_forward_hidden_states = self.mlp(hidden_states)
            hidden_states = (
                self.mlp_block_resid_gain * feed_forward_hidden_states
                + self.attn_block_resid_gain * attn_output
            )
            if self.add_mlp_skip:
                hidden_states += self.mlp_block_skip_gain * skip_branch

        else:
            # Attention residual connection
            hidden_states = self.attn_block_resid_gain * attn_output
            if self.add_attn_skip:
                hidden_states += self.attn_block_skip_gain * skip_branch

            if self.norm_position == "post":
                hidden_states = self.ln_2(hidden_states)

            skip_branch = hidden_states

            if self.norm_position == "pre":
                hidden_states = self.ln_2(hidden_states)

            feed_forward_hidden_states = self.mlp(hidden_states)

            # MLP residual connection
            hidden_states = self.mlp_block_resid_gain * feed_forward_hidden_states
            if self.add_mlp_skip:
                hidden_states += self.mlp_block_skip_gain * skip_branch

        return hidden_states


class SimplifiedAttention(nn.Module):
    """
    A customisable Attn sub-block that can implement Shaped Attention, and identity value/projection weights.
    """
    def __init__(self,
                 dim=256,
                 n_layer=12,
                 heads=8,
                 scale_attn_weights=False,
                 scale_attn_by_inverse_layer_idx=False,
                 first_layer_value_resid_gain=1,
                 value_resid_gain=0,
                 value_skip_gain=1,
                 val_init_type="id",
                 trainable_value_gains=True,
                 trainable_proj_gains=True,
                 last_layer_proj_resid_gain=None,
                 proj_resid_gain=0,
                 proj_skip_gain=1,
                 proj_init_type="id",
                 query_init_std=0,
                 key_init_std=None,
                 val_proj_init_std=None,
                 attn_mat_resid_gain=1,
                 trainable_attn_mat_gains=True,
                 attn_mat_skip_gain=1,
                 centre_attn=True,
                 centre_attn_gain=1,
                 attn_pdrop=0.1,
                 resid_pdrop=0.1,
                 decoder_only=False,
                 layer_idx=None):
        super().__init__()

        self.embed_dim = dim
        self.num_heads = heads
        self.head_dim = self.embed_dim // self.num_heads
        if self.head_dim * self.num_heads != self.embed_dim:
            raise ValueError(
                f"`embed_dim` must be divisible by num_heads (got `embed_dim`: {self.embed_dim} and `num_heads`:"
                f" {self.num_heads})."
            )

        self.scale_attn_weights = scale_attn_weights

        self.scale_attn_by_inverse_layer_idx = scale_attn_by_inverse_layer_idx
        self.layer_idx = layer_idx
        self.decoder_only = decoder_only

        self.qk_attn = SimplifiedConv1D(
            2 * self.embed_dim,
            self.embed_dim,
        )

        if first_layer_value_resid_gain is not None and layer_idx is not None and layer_idx == 0:
            value_resid_gain = first_layer_value_resid_gain
        else:
            value_resid_gain = value_resid_gain
        if (
            value_skip_gain != 1
            or value_resid_gain != 0
            or val_init_type != "id"
        ):
            self.v_attn = SimplifiedConv1D(
                self.embed_dim,
                self.embed_dim,
                resid_gain=value_resid_gain,
                skip_gain=value_skip_gain,
                trainable_gains=trainable_value_gains,
                init_type=val_init_type,
                bias=False,
            )
        else:
            self.v_attn = nn.Identity()

        if (
            last_layer_proj_resid_gain is not None
            and layer_idx is not None and layer_idx == n_layer - 1
        ):
            proj_resid_gain = last_layer_proj_resid_gain
        else:
            proj_resid_gain = proj_resid_gain
        if (
            proj_skip_gain != 1
            or proj_resid_gain != 0
            or proj_init_type != "id"
        ):
            self.c_proj = SimplifiedConv1D(
                self.embed_dim,
                self.embed_dim,
                resid_gain=proj_resid_gain,
                skip_gain=proj_skip_gain,
                trainable_gains=trainable_proj_gains,
                init_type=proj_init_type,
                bias=False,
            )
        else:
            self.c_proj = nn.Identity()

        self.split_size = self.embed_dim
        query_weight, key_weight = self.qk_attn.weight.data.split(
            self.split_size, dim=1
        )

        if query_init_std is not None:
            query_weight.normal_(mean=0.0, std=query_init_std)

        if key_init_std is not None:
            key_weight.normal_(mean=0.0, std=key_init_std)

        if val_proj_init_std is not None:
            self.v_attn.weight.data.normal_(mean=0.0, std=val_proj_init_std)
            self.c_proj.weight.data.normal_(mean=0.0, std=val_proj_init_std)

        self.attn_dropout = nn.Dropout(attn_pdrop)
        self.resid_dropout = nn.Dropout(resid_pdrop)

        self.pruned_heads = set()

        self.attn_mat_resid_gain = nn.Parameter(
            attn_mat_resid_gain * torch.ones((1, self.num_heads, 1, 1)),
            requires_grad=trainable_attn_mat_gains,
        )
        self.attn_mat_skip_gain = nn.Parameter(
            attn_mat_skip_gain * torch.ones((1, self.num_heads, 1, 1)),
            requires_grad=trainable_attn_mat_gains,
        )

        self.centre_attn = centre_attn
        self.centre_attn_gain = nn.Parameter(
            centre_attn_gain * torch.ones((1, self.num_heads, 1, 1)),
            requires_grad=trainable_attn_mat_gains
            and centre_attn_gain != 0,
        )

    def _attn(self, query, key, value, attention_mask=None):
        attn_weights = torch.matmul(query, key.transpose(-1, -2))

        if self.scale_attn_weights:
            attn_weights = attn_weights / torch.full(
                [],
                value.size(-1) ** 0.5,
                dtype=attn_weights.dtype,
                device=attn_weights.device,
            )

        # Layer-wise attention scaling
        if self.scale_attn_by_inverse_layer_idx and self.layer_idx is not None:
            attn_weights = attn_weights / float(self.layer_idx + 1)

        query_length, key_length = query.size(-2), key.size(-2)
        causal_mask = self.bias[
            :, :, key_length - query_length : key_length, :key_length
        ]
        mask_value = torch.finfo(attn_weights.dtype).min
        # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
        # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
        mask_value = torch.full([], mask_value, dtype=attn_weights.dtype).to(
            attn_weights.device
        )
        attn_weights = torch.where(
            causal_mask, attn_weights.to(attn_weights.dtype), mask_value
        )

        if attention_mask is not None:
            # Apply the attention mask
            attn_weights = attn_weights + attention_mask
        
        if self.decoder_only:
            """
            create a mask matrix with upper diagonal values all to be negative infinity so that
            one token only attends to itself and previous tokens
            """
            attn_weights_size = torch.Size([query.size(2), query.size(2)])
            attention_mask  = torch.zeros(attn_weights_size)
            attention_mask[:] = float('-inf')
            attention_mask = torch.triu(attention_mask, diagonal=1)
            attention_mask = attention_mask.unsqueeze(0).repeat(query.size(1), 1, 1)
            attention_mask = attention_mask.unsqueeze(0).repeat(query.size(0), 1, 1, 1)
            attn_weights = attn_weights + attention_mask

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        # Downcast (if necessary) back to V's dtype (if in mixed-precision) -- No-Op otherwise
        new_attn_weights = self.attn_mat_resid_gain * attn_weights.type(value.dtype)

        if self.centre_attn:
            post_sm_bias_matrix = (
                self.attn_mat_skip_gain * self.diag[:, :, :key_length, :key_length]
            ) - self.centre_attn_gain * (
                self.uniform_causal_attn_mat[
                    :, :, key_length - query_length : key_length, :key_length
                ]
            )
            new_attn_weights = new_attn_weights + post_sm_bias_matrix

        new_attn_weights = self.attn_dropout(new_attn_weights)

        attn_output = torch.matmul(new_attn_weights, value)

        return attn_output, attn_weights

    def _split_heads(self, tensor, num_heads, attn_head_size):
        """
        Splits hidden_size dim into attn_head_size and num_heads
        """
        new_shape = tensor.size()[:-1] + (num_heads, attn_head_size)
        tensor = tensor.view(new_shape)
        return tensor.permute(0, 2, 1, 3)  # (batch, head, seq_length, head_features)

    def _merge_heads(self, tensor, num_heads, attn_head_size):
        """
        Merges attn_head_size dim and num_attn_heads dim into hidden_size
        """
        tensor = tensor.permute(0, 2, 1, 3).contiguous()
        new_shape = tensor.size()[:-2] + (num_heads * attn_head_size,)
        return tensor.view(new_shape)

    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        val_len: Optional[torch.Tensor] = None,
        output_attentions: Optional[bool] = False,
    ) -> Tuple[torch.Tensor, ...]:

        max_positions = hidden_states.size(1)
        # Centered attention, from https://arxiv.org/abs/2306.1775
        uniform_causal_attn_mat = torch.ones(
            (max_positions, max_positions), dtype=torch.float32
        ) / torch.arange(1, max_positions + 1).view(-1, 1)
        self.register_buffer(
            "uniform_causal_attn_mat",
            torch.tril(
                uniform_causal_attn_mat,
            ).view(1, 1, max_positions, max_positions),
            persistent=False,
        )
        self.register_buffer(
            "diag",
            torch.eye(max_positions).view(1, 1, max_positions, max_positions),
            persistent=False,
        )
        self.register_buffer(
            "bias",
            torch.tril(
                torch.ones((max_positions, max_positions), dtype=torch.bool)
            ).view(1, 1, max_positions, max_positions),
            persistent=False,
        )

        (query, key) = self.qk_attn(hidden_states).split(self.split_size, dim=2)
        value = self.v_attn(hidden_states)

        query = self._split_heads(query, self.num_heads, self.head_dim)
        key = self._split_heads(key, self.num_heads, self.head_dim)
        value = self._split_heads(value, self.num_heads, self.head_dim)

        if type(val_len)  == torch.Tensor:
            """
            if the sequences in a minibatch have different valid length, then create an attention
            mask so that any tokens after the valid length for a sequence will not be in attention
            """
            attn_weights_size = torch.Size([query.size(0), query.size(1), query.size(2), query.size(2)])
            attention_mask  = torch.zeros(attn_weights_size)
            maxlen = hidden_states.size(1)
            mask = torch.arange(maxlen)[None, :] < val_len[:, None]
            mask = mask.unsqueeze(1).repeat(1, query.size(1), 1)
            mask = mask.unsqueeze(2).repeat(1, 1, query.size(2), 1)
            attention_mask[~mask] = float('-inf')
        else:
            attention_mask = None

        attn_output, attn_weights = self._attn(
            query, key, value, attention_mask
        )

        attn_output = self._merge_heads(attn_output, self.num_heads, self.head_dim)

        proj_output = self.c_proj(attn_output)
        proj_output = self.resid_dropout(proj_output)

        outputs = (proj_output,)
        if output_attentions:
            outputs += (attn_weights,)

        return outputs  # a, (attentions)


class SimplifiedMLP(nn.Module):
    def __init__(self, ff_mult, dim: int = 256, activation_function='leaky_relu',
                 lrelu_neg_slope: float = 0, resid_pdrop: float = 0.1, mlp_proj_init_std=None):

        """

        :param ff_mult:
        :type ff_mult:
        :param hidden_size:
        :type hidden_size: int
        :param activation_function:
        :type activation_function:
        :param lrelu_neg_slope:
        :type lrelu_neg_slope: float
        :param resid_pdrop:
        :type resid_pdrop: float
        :param mlp_proj_init_std:
        :type mlp_proj_init_std:
        """

        super().__init__()
        embed_dim = dim
        intermediate_size = dim*ff_mult

        self.c_fc = SimplifiedConv1D(intermediate_size, embed_dim, bias=False)
        self.c_proj = SimplifiedConv1D(embed_dim, intermediate_size, bias=False)

        if activation_function != "leaky_relu":
            self.act = ACT2FN[activation_function]
        else:
            self.act = LeakyReLU(negative_slope=lrelu_neg_slope)

        self.dropout = nn.Dropout(resid_pdrop)

        if mlp_proj_init_std is not None:
            nn.init.normal_(self.c_proj.weight, std=mlp_proj_init_std)

    def forward(self, hidden_states: Optional[Tuple[torch.FloatTensor]]) -> torch.FloatTensor:
        """

        :param hidden_states:
        :type hidden_states: Optional[Tuple[torch.FloatTensor]]
        :return:
        :rtype: torch.Tensor
        """
        hidden_states = self.c_fc(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.c_proj(hidden_states)
        hidden_states = self.dropout(hidden_states)
        return hidden_states


class SimplifiedConv1D(nn.Module):
    """
    (Linear) 1D-convolutional layer that can be reparameterised into skip (see Eq. 6 of paper).
    """

    def __init__(self, nf, nx, resid_gain: float = None, skip_gain: float = None, trainable_gains: bool = False,
                 init_type: str = "normal", bias: bool = True):

        """
        :param nf: number of output features
        :type nf: int
        :param nx: number of input features
        :type nx: int
        :param resid_gain: Residual weight
        :type resid_gain: float
        :param skip_gain: Skip weight, if None then defaults to standard Linear layer
        :type skip_gain: float
        :param trainable_gains:  Whether gains are trainable
        :type trainable_gains: bool
        :param init_type: (one of ["orth", "id", "normal"]): Type of weight initialisation.
        :type init_type: str
        :param bias: Whether to use bias parameters.
        :type bias: bool
        """
        super().__init__()
        self.nf = nf

        if bias:
            self.bias = nn.Parameter(torch.zeros(nf))
        else:
            self.bias = nn.Parameter(torch.zeros(nf), requires_grad=False)
        
        if skip_gain is None:
            # Standard linear layer
            self.weight = nn.Parameter(torch.empty(nx, nf))
            if init_type == "orth":
                nn.init.orthogonal_(self.weight)
            elif init_type == "id":
                self.weight.data = torch.eye(nx)
            elif init_type == "normal":
                nn.init.normal_(self.weight, std=0.02)
            else:
                raise NotImplementedError
            self.skip = False

        elif skip_gain is not None:
            # Reparameterised linear layer
            assert nx == nf
            self.resid_gain = nn.Parameter(
                torch.Tensor([resid_gain]), requires_grad=trainable_gains
            )
            self.skip_gain = nn.Parameter(
                torch.Tensor([skip_gain]),
                requires_grad=trainable_gains,
            )

            self.weight = nn.Parameter(torch.zeros(nx, nx))
            if init_type == "orth":
                self.id = nn.init.orthogonal_(torch.empty(nx, nx))
            elif init_type == "id":
                self.id = torch.eye(nx)
            elif init_type == "normal":
                self.id = nn.init.normal_(
                    torch.empty(nx, nx), std=1 / math.sqrt(nx)
                )
            else:
                raise NotImplementedError
            self.skip = True
            self.init_type = init_type

    def forward(self, x):
        """

        :param x:
        :type x: torch.Tensor
        :return:
        :rtype: torch.Tensor
        """
        size_out = x.size()[:-1] + (self.nf,)
        if self.skip:
            self.id = self.id.to(self.skip_gain.device)
            if self.resid_gain == 0 and self.init_type == "id":
                x = torch.add(self.bias, x * self.skip_gain)
            else:
                x = torch.addmm(
                    self.bias,
                    x.view(-1, x.size(-1)),
                    self.resid_gain * self.weight + self.skip_gain * self.id,
                )
        else:
            x = torch.addmm(self.bias, x.view(-1, x.size(-1)), self.weight)
        x = x.view(size_out)

        return x
