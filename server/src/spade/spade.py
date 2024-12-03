from server.src.classifier.classifier import Classifier
from server.src.gui.SpadeAssistant import SpadeAssistant
from server.src.game.game_round import GameRound
from server.src.game.hand_analysis.poker_hand_analyzer import PokerHandAnalyzer


class Spade:
    def __init__(self):
        self.classifier = Classifier("model_99_.pt")
        self.spade_assistant = SpadeAssistant
        self.game = GameRound
        self.hand_analyser = PokerHandAnalyzer

        pass

    def start(self):
        pass
