# IMPORTS
import torch
from src.classifier.model.spadeClassifier import SpadeClassifier
import matplotlib.pyplot as plt
import os

from src.game.resources.card import Card, Suit, Rank

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
torch.cuda.set_per_process_memory_fraction(0.8, device=0)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


class Classifier:
    def __init__(self, model_path: str):
        self.model = SpadeClassifier().to(device)
        self.model.load_state_dict(torch.load(os.path.join("pretrained_models", model_path), weights_only=True))

    def predict(self, image) -> list[Card]:
        #Scale Image

        #Pass to Model
        images = image.to(device)

        # Forward pass
        outputs = self.model(images)

        #valuate Output
        cards = []
        for output in outputs:
            suit = Suit[""]
            rank = Rank[""]
            cards.append(Card(suit, rank))
        # return cards
        return cards
