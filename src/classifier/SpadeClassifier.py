"""
SpadeClassifier.py
Uses a simplified ResNet architecture to classify playing cards.
It has 42 layers and uses BatchNorm2d as normalization layer, ReLU as activation function.
The output of the model is a probability distribution over the 53 possible playing cards.
"""

import torch
import torch.nn as nn
from torch import Tensor


def conv3x3(in_features: int, out_features: int, stride=1) -> nn.Conv2d:
    """3x3 convolution with padding"""
    return nn.Conv2d(in_features, out_features, stride=stride, kernel_size=3, padding=1, bias=False)


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
        self.conv1 = conv3x3(in_features, out_features, stride=stride)
        self.bn1 = nn.BatchNorm2d(out_features)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(out_features, out_features)
        self.bn2 = nn.BatchNorm2d(out_features)

        # Downsample Layer
        if downsample:
            self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Matching identity to output if in and out features differ
        if in_features != out_features:
            self.identity_matching = conv3x3(in_features, out_features)
        else:
            self.identity_matching = None

    def forward(self, x: Tensor) -> Tensor:
        identity = x
        if self.identity_matching:
            identity = self.identity_matching(identity)
        if self.downsample:
            identity = self.maxpool(identity)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        out += identity
        out = self.relu(out)

        return out


class SpadeClassifier(torch.nn.Module):
    def __init__(self, num_classes: int) -> None:
        super().__init__()
        features = [64, 64, 128, 256, 512]
        num_layers = [2 for _ in range(4)]
        self.conv1 = nn.Conv2d(3, features[0], kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(features[0])
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(64, 64, num_layers[0])
        self.layer2 = self._make_layer(64, 128, num_layers[1], downsample=True)
        self.layer3 = self._make_layer(128, 256, num_layers[2], downsample=True)
        self.layer4 = self._make_layer(256, 512, num_layers[3], downsample=True)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    @staticmethod
    def _make_layer(in_features: int, features: int, num_layers: int, downsample: bool = False) -> nn.Sequential:
        layers = []

        # First layer downsamples the image and changes the features
        first_layer = Block(in_features, features, downsample)
        layers.append(first_layer)
        in_features = features
        for _ in range(1, num_layers):
            layers.append(Block(in_features, features))
        return nn.Sequential(*layers)

    def forward(self, x: Tensor) -> Tensor:
        # Preprocessing
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        # Main feature extraction
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        # Encoder
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        x = torch.softmax(x, dim=1)

        return x
