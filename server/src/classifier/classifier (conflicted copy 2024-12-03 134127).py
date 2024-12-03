# IMPORTS
import torch
from src.classifier.model.spadeClassifier import SpadeClassifier
import matplotlib.pyplot as plt
import os

from src.game_logic.resources.card import Card, Suit, Rank

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'


class Classifier:
    def __init__(self, model_path: str):
        self.model = SpadeClassifier().to(device)
        # Choose the appropriate device based on CUDA availability

        # Load the model state with appropriate map_location
        self.model.load_state_dict(
            torch.load(os.path.join("src/classifier/pretrained_models/", model_path), map_location=device,
                       weights_only=True))

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
