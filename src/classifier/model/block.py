"""
This is a simplified version of the BasicBlock class from Resnet:
https://github.com/pytorch/vision/blob/main/torchvision/models/resnet.py
"""

import torch
import torch.nn as nn
from torch import Tensor


class Block(nn.Module):
    """
    Basic Block for SpadeClassifier Architecture.
    Conv -> BatchNorm -> ReLU -> Conv -> BatchNorm -> Concat with Input -> ReLU
    """
    def __init__(self, in_features, out_features, downsample: bool = False) -> None:
        super().__init__()

        # Add a stride if spatial dimension gets downsampled
        stride = 2 if downsample else 1

        # Conv
        self.downsample = downsample
        self.conv1 = self.conv3x3(in_features, out_features, stride=stride)
        self.bn1 = nn.BatchNorm2d(out_features)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = self.conv3x3(out_features, out_features)
        self.bn2 = nn.BatchNorm2d(out_features)
        self.identity_matching = self.conv3x3(in_features, out_features, stride=stride)

    @staticmethod
    def conv3x3(in_features: int, out_features: int, stride=1) -> nn.Conv2d:
        """3x3 convolution with padding"""
        return nn.Conv2d(in_features, out_features, stride=stride, kernel_size=3, padding=1, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        identity = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x)

        # Match shape of identity to output shape
        if x.shape != identity.shape:
            identity = self.identity_matching(identity)

        x += identity
        x = self.relu(x)

        return x
