# IMPORTS
import torch
from dataset import PlayingCardDataset
from torch.utils.data import DataLoader
from src.classifier.model.spadeClassifier import SpadeClassifier
import matplotlib.pyplot as plt
import os

from src.game.resources.card import Card, Suit, Rank


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
torch.cuda.set_per_process_memory_fraction(0.8, device=0)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


class Classifier:
    def __init__(self, model: str):
        model = SpadeClassifier().to(device)
        model.load_state_dict(torch.load("pretrained_models/" + model, weights_only=True))

    def predict(self, image) -> Card:
        #Scale Image

        #Pass to Model
        images = image.to(device)

        # Forward pass
        outputs = self.model(images)

        #valuate Output
        suit = Suit[""]
        rank = Rank[""]
        return Card(suit, rank)