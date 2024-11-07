"""
spadeClassifier.py
Uses a simplified ResNet architecture to classify playing cards.
It has 42 layers and uses BatchNorm2d as normalization layer, ReLU as activation function.
The output of the model is a probability distribution over the 53 possible playing cards.
"""

import torch.nn as nn
from torch import Tensor
from src.classifier.model.block import Block
from src.classifier.model.head import Head


class SpadeClassifier(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        features = [64, 64, 128, 256, 512]
        num_layers = [3 for _ in range(4)]
        self.conv1 = nn.Conv2d(3, features[0], kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(features[0])
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(features[1], features[1], num_layers[0])
        self.layer2 = self._make_layer(features[1], features[2], num_layers[1], downsample=True)
        self.layer3 = self._make_layer(features[2], features[3], num_layers[2], downsample=True)
        self.layer4 = self._make_layer(features[3], features[4], num_layers[3], downsample=True)
        self.head = Head(features[4])

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

        # Head
        x = self.head(x)

        return x



