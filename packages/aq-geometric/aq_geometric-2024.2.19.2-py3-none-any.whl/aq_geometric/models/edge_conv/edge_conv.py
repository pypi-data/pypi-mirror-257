from typing import List, Union

import uuid
import torch
import torch.nn.functional as F
from torch.nn import Sequential as Seq, Linear, ReLU
from torch_geometric.nn import MessagePassing

from aq_geometric.models.base_model import BaseModel


class EdgeConv(MessagePassing):
    r"""EdgeConv layer for predicting air quality.
    
    This basic EdgeConv implementation is based on the following paper:
    https://arxiv.org/abs/1801.07829
    """
    def __init__(self, in_channels: int, out_channels: int, aggr: str = "max"):
        super().__init__(aggr=aggr)
        self.mlp = Seq(Linear(2 * in_channels, out_channels), ReLU(),
                       Linear(out_channels, out_channels))

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor):
        # x has shape [N, in_channels]
        # edge_index has shape [2, E]

        return self.propagate(edge_index, x=x)

    def message(self, x_i: torch.Tensor, x_j: torch.Tensor):
        # x_i has shape [E, in_channels]
        # x_j has shape [E, in_channels]

        tmp = torch.cat([x_i, x_j - x_i],
                        dim=1)  # tmp has shape [E, 2 * in_channels]
        return self.mlp(tmp)


class EdgeConvModel(BaseModel):
    r"""EdgeConv model for predicting air quality.
    
    This basic EdgeConv implementation is based on the following paper:
    https://arxiv.org/abs/1801.07829
    
    Args:
        name (str): The name of the model.
        guid (str): The unique identifier for the model.
        stations (list): The list of stations to use for the model.
        in_channels (int): The number of input channels.
        out_channels (int): The number of output channels.
        linear_hidden (int): The number of hidden units for the linear layer.
        linear_out (int): The number of output units for the linear layer.    
    """
    def __init__(
        self,
        name: str = "EdgeConvModel",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        in_channels: int = 48,
        out_channels: int = 256,
        aggr: str = "max",
        linear_hidden: int = 16,
        linear_out: int = 1,
    ):
        super().__init__(name=name, guid=guid, stations=stations)
        self.conv1 = EdgeConv(in_channels, out_channels, aggr)
        self.conv2 = EdgeConv(out_channels, out_channels, aggr)
        self.conv3 = EdgeConv(out_channels, out_channels, aggr)
        self.max_pool = torch.nn.MaxPool1d(in_channels)
        self.fc = torch.nn.Linear(
            linear_hidden, linear_out
        )  # shape of the input to the linear layer is 8 for 128 hidden units and 16 for 256?

    def forward(self, x, edge_index):
        """Define the forward pass for the EdgeConv model."""
        # forward pass through the edge convolutions
        x_1 = self.conv1(x, edge_index)
        x_2 = x_1.relu()
        x_3 = self.conv2(x_2, edge_index)
        x_4 = x_3.relu()
        x_5 = self.conv3(x_4, edge_index)
        x_6 = x_5.relu()

        # concatenate
        x_7 = torch.cat((x_2, x_4, x_6), dim=1)

        # max pool
        x_8 = self.max_pool(x_7)

        # linear
        x_9 = self.fc(x_8)

        return x_9
