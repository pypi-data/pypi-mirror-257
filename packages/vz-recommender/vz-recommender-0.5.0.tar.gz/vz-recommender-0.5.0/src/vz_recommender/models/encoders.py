import torch
import torch.nn as nn
import torch.nn.functional as F


class VariationalEncoder(nn.Module):

    def __init__(self, latent_dims: int, input_dim: int):
        """

        :param latent_dims: specify an integer for the latent or hidden dimensions
        :param input_dim: an integer value for input dimensions
        """
        super().__init__()
        self.linear1 = nn.Linear(input_dim, input_dim // 2)
        self.linear2 = nn.Linear(input_dim // 2, latent_dims)
        self.linear3 = nn.Linear(input_dim // 2, latent_dims)
        self.input_dim = input_dim

        self.N = torch.distributions.Normal(0, 1)
        self.kl = 0

    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        This method takes in input data and maps it to the latent space (representation of compressed data)
        using a neural network. Loss function is the KL divergence loss between the sampled distribution and the prior
        distribution.

        :param x: `torch.tensor` this is the input tensor that needs to be encoded to the latent_dims (batch_size, input_dim)
        :return: `torch.tensor` the output tensor representing the mapped input data in the latent space (batch_size, latent_dims)
        """
        x = F.relu(self.linear1(x))
        mu = self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma * self.N.sample(mu.shape).to(x.device)
        self.kl = (sigma ** 2 + mu ** 2 - torch.log(sigma) - 1 / 2).sum()
        return z  # , self.kl


class Decoder(nn.Module):
    """
    This class defines a decoder module for a deep learning model. It takes in a latent dimension (usually lower
    dimension) and an input dimension and returns a decoded output. For a full working example, please check for
    AutoEncoderPL implementation in this file personalization-ai/search_reco/ai_search/models.py
    """

    def __init__(self, latent_dims: int, input_dim: int) -> None:
        """
        :param latent_dims: The dimension of the latent space.
        :param input_dim: The dimension of the input space.
        """
        super().__init__()
        self.linear1 = nn.Linear(latent_dims, input_dim // 2)
        self.linear2 = nn.Linear(input_dim // 2, input_dim)
        self.latent_dims = latent_dims

    def forward(self, z: torch.tensor) -> torch.tensor:
        """
        Takes an input tensor and returns a decoded tensor of the same and applies linear and non linear transformations
        :param z: tensor to be decoded
        :return: decoded tensor
        """
        z = F.relu(self.linear1(z))
        z = torch.sigmoid(self.linear2(z))
        return z


class LinearVAE(nn.Module):
    """
    This class implements a Linear Variational Autoencoder (VAE) using PyTorch. It consists of an encoder and a decoder,
    both of which are implemented as separate modules. The encoder takes in an input tensor and produces a latent
    representation (compressed representation), while the decoder takes in the latent representation and produces a
    reconstructed output tensor. The VAE is trained to minimize the reconstruction error while also regularizing the
    latent representation to follow a prior distribution (usually a standard normal distribution).

    for usage examples, refer to:  search_reco/ai_search/models.py
    """

    def __init__(self, latent_dims: int, input_dim: int) -> None:
        """
        Initializes the LinearVAE class by creating an instance of the VariationalEncoder and Decoder classes.

        :param latent_dims: The dimension of the latent space.
        :param input_dim: The dimension of the input space.
        """

        super().__init__()
        self.encoder = VariationalEncoder(latent_dims=latent_dims, input_dim=input_dim)
        self.decoder = Decoder(latent_dims=latent_dims, input_dim=input_dim)

    def forward(self, x: torch.tensor) -> torch.tensor:
        """
        performs a forward pass through the LinearVAE model by passing the input tensor through the encoder to obtain
        a latent representation, and then passing the latent representation through the decoder to obtain a
        reconstructed output tensor. The reconstructed output tensor is returned

        :param x: input for the encoder instance's forward, the output from this becomes input for the decoder instance
        :return: reconstructed output from the decder
        """
        z = self.encoder(x)
        return self.decoder(z)  # , kl
