from src.classifier.classifier import Classifier
from src.gui.SpadeAssistant import SpadeAssistant
from src.game.game_round import GameRound
from src.game.hand_analysis.poker_hand_analyzer import PokerHandAnalyzer


class Spade:
    def __init__(self):
        self.classifier = Classifier("model_99_.pt")
        self.spade_assistant = SpadeAssistant
        self.game = GameRound
        self.hand_analyser = PokerHandAnalyzer

        pass

    def start(self):
        pass
