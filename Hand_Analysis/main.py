from Hand_Analysis.card import Card, Rank, Suit
from Hand_Analysis.player import Player
from Hand_Analysis.winner_analyzer import WinnerAnalyzer

if __name__ == "__main__":
    # Create player instances
    player1 = Player("Alice")
    player2 = Player("Bob")
    player3 = Player("Jonas")

    # Players receive their cards
    player1.receive_card(Card(Suit.DIAMONDS, Rank.SEVEN))
    player1.receive_card(Card(Suit.CLUBS, Rank.ACE))  # Fixed this line to match the format

    player2.receive_card(Card(Suit.CLUBS, Rank.SEVEN))
    player2.receive_card(Card(Suit.HEARTS, Rank.ACE))

    player3.receive_card(Card(Suit.CLUBS, Rank.SEVEN))
    player3.receive_card(Card(Suit.SPADES, Rank.ACE))

    # Set community cards (for example)
    community_cards = [
        Card(Suit.SPADES, Rank.TWO),
        Card(Suit.CLUBS, Rank.THREE),
        Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.DIAMONDS, Rank.ACE)
    ]

    # Get the best hand for each player
    best_hand1 = player1.get_best_hand(community_cards)[1]
    best_hand2 = player2.get_best_hand(community_cards)[1]
    best_hand3 = player3.get_best_hand(community_cards)[1]

    print(f"{player1.name}'s Best Hand: {best_hand1}")
    print(f"{player2.name}'s Best Hand: {best_hand2}")
    print(f"{player3.name}'s Best Hand: {best_hand3}")


    # To find winners, you would integrate this with WinnerAnalyzer
    analyzer = WinnerAnalyzer([(player1.name, best_hand1), (player2.name, best_hand2), (player3.name, best_hand3)])
    winners = analyzer.analyze_winners()

    print("Winners:")
    for winner in winners:
        print(winner)
