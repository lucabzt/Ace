import random

from src.game.hand_analysis.winner_determiner import WinnerAnalyzer
from src.game.resources.card import Card, Suit, Rank
from src.game.resources.player import Player


# Create a full deck of cards
def create_deck():
    """Create a full deck of cards."""
    return [Card(suit, rank) for suit in Suit for rank in Rank]


def draw_random_card(deck):
    """Draw a random card from the deck and remove it to avoid duplicates."""
    card = random.choice(deck)
    deck.remove(card)  # Remove the card from the deck
    return card


def generate_random_hand(deck, num_cards=2):
    """Generate a random hand of cards for a player."""
    return [draw_random_card(deck) for _ in range(num_cards)]


def generate_random_community_cards(deck, num_cards=5):
    """Generate random community cards."""
    return [draw_random_card(deck) for _ in range(num_cards)]


def main():
    # Create a full deck of cards
    deck = create_deck()

    # Create player instances, including Markus and Luca
    players = [Player("Huber"), Player("Rogg"), Player("Hoerter"), Player("Vorderbrügge"), Player("Huber"), Player("Bozzetti"), Player("Simon"), Player("Maier")]

    # Players receive their cards
    for player in players:
        cards = generate_random_hand(deck)
        player.receive_card(cards[0])
        player.receive_card(cards[1])
        print(f"{player.name} received: {cards[0]} and {cards[1]}")

    print("----------------------------------------")
    print(" ")

    # Generate community cards
    community_cards = generate_random_community_cards(deck)
    print("Community Cards:", community_cards)
    print(" ")

    # Get the best hand for each player
    best_hands = []
    for player in players:
        best_hand = player.get_best_hand(community_cards)
        best_hands.append((player.name, best_hand[0], best_hand[1]))  # Store the player's name, hand type, and cards

    # Print each player's best hand
    for player_name, hand_type, best_hand in best_hands:
        print(f"{player_name}'s Best Hand: {hand_type} with cards {sorted(best_hand)}")

    # To find winners, you would integrate this with WinnerAnalyzer
    analyzer = WinnerAnalyzer([(player_name, best_hand) for player_name, _, best_hand in best_hands])
    winners = analyzer.analyze_winners()

    print(" ")
    print("Winners:")
    for winner in winners:
        print(winner)

    return winners


if __name__ == "__main__":
    main()
