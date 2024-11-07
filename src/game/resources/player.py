from src.game.hand_analysis.poker_hand_analyzer import PokerHandAnalyzer


class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.cards = []  # Player's own cards
        self.balance = balance  # Player's balance for betting

    def receive_card(self, card):
        """Adds a card to the player's hand, limited to 2 cards."""
        if len(self.cards) < 2:
            if card in self.cards:
                raise Exception("Duplicate card found in " + self.name)
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
        self.cards.sort()
        return ', '.join(str(card) for card in self.cards)

    def clear_cards(self):
        """Resets the player's hand and community cards."""
        self.cards = []

    def add_balance(self, amount):
        """Increases the player's balance by the specified amount."""
        if amount < 0:
            raise ValueError("Cannot add a negative amount to balance.")
        self.balance += amount

    def deduct_balance(self, amount):
        """Decreases the player's balance by the specified amount."""
        if amount < 0:
            raise ValueError("Cannot deduct a negative amount from balance.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

    def __str__(self):
        return f"Player: {self.name}, Balance: ${self.balance}, Cards: {self.show_cards()}"
