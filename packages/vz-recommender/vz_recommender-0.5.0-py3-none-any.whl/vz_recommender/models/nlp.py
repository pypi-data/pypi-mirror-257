import torch
from torch import nn
from transformers import AutoModel


import sys, os
sys.path.insert(0, os.path.abspath("../models/"))
from .transformer import ParallelTransformerBlock
from .moe import ExpertLayer, MoEFFLayerTopK


class GRecRTS(nn.Module):
    def __init__(self, nlp_dim, nlp_encoder_path, task_dims, moe_kwargs=None):
        super().__init__()

        self.nlp_dim = nlp_dim
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)

        self.moe = MoEFFLayerTopK(
            dim=nlp_dim,
            num_experts=moe_kwargs.get("num_experts"),
            expert_capacity=moe_kwargs.get("expert_capacity"),
            router_jitter_noise=moe_kwargs.get("router_jitter_noise"),
            hidden_size=nlp_dim,
            expert_class=ExpertLayer,
            num_K=moe_kwargs.get("num_K"),
        )

        self.task_dense_0 = nn.ModuleDict()
        self.task_dropout = nn.Dropout(p=0.1)
        self.task_dense_1 = nn.ModuleDict()
        self.task_embedding = nn.Embedding(len(task_dims), nlp_dim)
        self.task_act_1 = nn.LeakyReLU(0.2)
        for i, dim in enumerate(task_dims):
            self.task_dense_0[f"task{i}"] = nn.Linear(
                in_features=nlp_dim,
                out_features=nlp_dim // 2
            )
            self.task_dense_1[f"task{i}"] = nn.Linear(
                in_features=nlp_dim // 2,
                out_features=dim
            )

        self.out_act = nn.Sigmoid()

    def split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(3):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.task_dense_0[f"task{i}"](task_input)
            task_out = self.task_act_1(task_out)
            task_out = self.task_dropout(task_out)
            task_out = self.task_dense_1[f"task{i}"](task_out)
            task_indices.append(task_indice)
            task_outs.append(task_out)
        return task_indices, task_outs

    def forward(self, nlp_in, task_in):
        """
        Args:

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        nlp_out = self.nlp_encoder(**nlp_in).pooler_output.to(dtype=torch.float32)
        task_out = self.task_embedding(task_in)
        nlp_out = nlp_out[:, None, :]
        task_out = task_out[:, None, :]
        outs, aux_loss = self.moe(nlp_out, task_out)
        outs = outs.reshape(-1, self.nlp_dim)
        task_indices, task_outs = self.split_task(task_in, outs)
        return tuple(task_indices), tuple(task_outs), aux_loss


class GRecConcatRTS(nn.Module):
    def __init__(self, nlp_dim, nlp_encoder_path, task_dims, moe_kwargs=None):
        super().__init__()

        self.nlp_dim = nlp_dim
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)

        self.att_pooling = ParallelTransformerBlock(
            dim=nlp_dim, dim_head=nlp_dim, heads=1
        )

        self.moe = MoEFFLayerTopK(
            dim=nlp_dim,
            num_experts=moe_kwargs.get("num_experts"),
            expert_capacity=moe_kwargs.get("expert_capacity"),
            router_jitter_noise=moe_kwargs.get("router_jitter_noise"),
            hidden_size=nlp_dim,
            expert_class=ExpertLayer,
            num_K=moe_kwargs.get("num_K"),
        )

        self.task_dense_0 = nn.ModuleDict()
        self.task_dense_1 = nn.ModuleDict()
        self.task_embedding = nn.Embedding(len(task_dims), nlp_dim)
        self.task_act_1 = nn.LeakyReLU(0.2)
        for i, dim in enumerate(task_dims):
            self.task_dense_0[f"task{i}"] = nn.Linear(
                in_features=nlp_dim * 2,
                out_features=nlp_dim // 2
            )
            self.task_dense_1[f"task{i}"] = nn.Linear(
                in_features=nlp_dim // 2,
                out_features=dim
            )

        self.out_act = nn.Sigmoid()

    def split_task(self, task_in, combined_out):
        task_indices = []
        task_outs = []
        for i in range(3):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_input = combined_out[task_indice]
            task_out = self.task_dense_0[f"task{i}"](task_input)
            task_out = self.task_act_1(task_out)
            task_out = self.task_dense_1[f"task{i}"](task_out)
            task_indices.append(task_indice)
            task_outs.append(task_out)
        return task_indices, task_outs

    def forward(self, nlp_in, task_in):
        """
        Args:

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        nlp_out = self.nlp_encoder(**nlp_in).pooler_output.to(dtype=torch.float32)
        task_out = self.task_embedding(task_in)
        out = torch.stack([task_out, nlp_out], dim=1)
        out = self.att_pooling(out)
        out, aux_loss = self.moe(out)
        outs = torch.concat(out.unbind(1), dim=1)
        task_indices, task_outs = self.split_task(task_in, outs)
        return tuple(task_indices), tuple(task_outs), aux_loss


class SearchIntent(nn.Module):
    def __init__(self, nlp_dim, out_dim, nlp_encoder_path):
        super().__init__()

        self.nlp_dim = nlp_dim
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.dense_0 = nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_dim // 2
        )
        self.dense_1 = nn.Linear(
            in_features=nlp_dim // 2,
            out_features=out_dim
        )
        self.act = nn.LeakyReLU(0.2)
#         self.softmax = nn.Softmax(dim=1)

    def forward(self, nlp_in):
        """
        Args:

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        nlp_out = self.nlp_encoder(**nlp_in).pooler_output.to(dtype=torch.float32)
        out = self.dense_0(nlp_out)
        out = self.act(out)
        out = self.dense_1(out)
#         out = self.softmax(out)
        return out
