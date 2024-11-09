"""
Simple head for the playing card classifier. Takes the extracted features as input
and outputs a probability distribution over:
14 Ranks (Ace-King), 14 is the Joker
4 Suits (Spades, Clubs, Diamonds, Hearts)
Idea to improve: https://github.com/luuuyi/CBAM.PyTorch/blob/master/model/resnet_cbam.py
"""

import torch
import torch.nn as nn
from torch import Tensor


class Head (nn.Module):
    def __init__ (self, in_features) -> None:
        super().__init__()
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(in_features, 53)

    def forward(self, x) -> Tensor:
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x
