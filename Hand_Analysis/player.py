from Hand_Analysis.card import Card  # Import your Card class
from Hand_Analysis.hand_analyzer import PokerHandAnalyzer  # Assuming your PokerHandAnalyzer is in this module


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []  # Player's own cards

    def receive_card(self, card):
        """Adds a card to the player's hand, limited to 2 cards."""
        if len(self.cards) < 2:
            self.cards.append(card)
        else:
            raise Exception("Player already has 2 cards.")

    def get_best_hand(self, community_cards):
        """Calculates the best hand the player can make with their cards and community cards."""
        if len(self.cards) != 2 or len(community_cards) != 5:
            raise ValueError("Player must have 2 cards and there must be 5 community cards.")

        all_cards = self.cards + community_cards  # Combine player's cards with community cards
        analyzer = PokerHandAnalyzer(all_cards)  # Create an instance of the PokerHandAnalyzer
        best_hand_type, best_hand_cards = analyzer.get_best_hand()  # Get the best hand type and cards

        return best_hand_type, best_hand_cards

    def show_cards(self):
        """Returns a string representation of the player's cards."""
        return ', '.join(str(card) for card in self.cards)

    def clear_cards(self):
        """Resets the player's hand and community cards."""
        self.cards = []

    def __str__(self):
        return f"Player: {self.name}, Cards: {self.show_cards()}"
