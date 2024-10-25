from Hand_Analysis.card import Card, Rank, Suit
from Hand_Analysis.player import Player
from Hand_Analysis.winner_analyzer import WinnerAnalyzer

if __name__ == "__main__":
    # Create player instances
    player1 = Player("Alice")
    player2 = Player("Bob")

    # Players receive their cards
    player1.receive_card(Card(Suit.HEARTS, Rank.ACE))
    player1.receive_card(Card(Suit.HEARTS, Rank.KING))  # Fixed this line to match the format

    player2.receive_card(Card(Suit.CLUBS, Rank.KING))
    player2.receive_card(Card(Suit.CLUBS, Rank.QUEEN))

    # Set community cards (for example)
    community_cards = [
        Card(Suit.DIAMONDS, Rank.TEN),   # Use Card class directly for community cards
        Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.SPADES, Rank.EIGHT),
        Card(Suit.DIAMONDS, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.SIX)
    ]

    # Get the best hand for each player
    best_hand1 = player1.get_best_hand(community_cards)[1]
    best_hand2 = player2.get_best_hand(community_cards)[1]

    print(f"{player1.name}'s Best Hand: {best_hand1}")
    print(f"{player2.name}'s Best Hand: {best_hand2}")

    # To find winners, you would integrate this with WinnerAnalyzer
    analyzer = WinnerAnalyzer([(player1.name, best_hand1), (player2.name, best_hand2)])
    winners = analyzer.analyze_winners()

    print("Winners:")
    for winner in winners:
        print(winner)
