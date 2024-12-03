import random

from server.src.game.resources.card import Card, Suit, Rank


class Deck:

    """Create a randomly shuffled deck of cards"""
    def __init__(self):
        """Initialisiert ein Standard-Pokerdeck mit 52 Karten basierend auf den Suit- und Rank-Enums."""
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self):
        """Mischt das Deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Gibt die oberste Karte vom Deck zurück."""
        if len(self.cards) == 0:
            raise Exception("Das Deck ist leer.")
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck mit {len(self.cards)} Karten: {self.cards}"
