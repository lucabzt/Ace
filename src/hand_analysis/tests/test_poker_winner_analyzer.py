import unittest
from hand_analysis.resources.card import Card, Rank, Suit
from hand_analysis.resources.player import Player
from hand_analysis.analysis.winner_analyzer import WinnerAnalyzer


class TestWinnerAnalyzer(unittest.TestCase):

    # test case for Royal Flush vs. Four of a Kind
    def test_royal_flush_vs_four_of_a_kind(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Royal Flush
        player1.receive_card(Card(Suit.SPADES, Rank.ACE))
        player1.receive_card(Card(Suit.SPADES, Rank.KING))

        # Bob has Four of a Kind
        player2.receive_card(Card(Suit.HEARTS, Rank.FOUR))
        player2.receive_card(Card(Suit.CLUBS, Rank.FOUR))

        community_cards = [
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.DIAMONDS, Rank.FOUR),
            Card(Suit.SPADES, Rank.FOUR)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Royal Flush vs. Four of a Kind test failed")

    # test case for Split Pot with Full House
    def test_full_house_split_pot(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Both Alice and Bob have the same Full House
        player1.receive_card(Card(Suit.SPADES, Rank.THREE))
        player1.receive_card(Card(Suit.HEARTS, Rank.THREE))

        player2.receive_card(Card(Suit.DIAMONDS, Rank.THREE))
        player2.receive_card(Card(Suit.CLUBS, Rank.THREE))

        community_cards = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.FOUR)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"}, "Full House split pot test failed")

    # test case for Straight Flush vs. Flush
    def test_straight_flush_vs_flush(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Straight Flush
        player1.receive_card(Card(Suit.CLUBS, Rank.SIX))
        player1.receive_card(Card(Suit.CLUBS, Rank.FIVE))

        # Bob has a Flush
        player2.receive_card(Card(Suit.HEARTS, Rank.KING))
        player2.receive_card(Card(Suit.HEARTS, Rank.NINE))

        community_cards = [
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.NINE),
            Card(Suit.HEARTS, Rank.TWO),
            Card(Suit.HEARTS, Rank.THREE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Straight Flush vs. Flush test failed")

    # test case for Split Pot with High Card
    def test_high_card_split_pot(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice and Bob both have the highest card Ace, but no other hand ranks
        player1.receive_card(Card(Suit.HEARTS, Rank.ACE))
        player1.receive_card(Card(Suit.CLUBS, Rank.TWO))

        player2.receive_card(Card(Suit.SPADES, Rank.ACE))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.THREE))

        community_cards = [
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.SIX),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.EIGHT)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"}, "High Card split pot test failed")

    # test case for Flush vs. Two Pair
    def test_flush_vs_two_pair(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Flush
        player1.receive_card(Card(Suit.HEARTS, Rank.ACE))
        player1.receive_card(Card(Suit.HEARTS, Rank.FIVE))

        # Bob has Two Pair
        player2.receive_card(Card(Suit.SPADES, Rank.TEN))
        player2.receive_card(Card(Suit.CLUBS, Rank.TEN))

        community_cards = [
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.THREE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Flush vs. Two Pair test failed")

    # test case for Full House vs. Straight
    def test_full_house_vs_straight(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Full House
        player1.receive_card(Card(Suit.SPADES, Rank.KING))
        player1.receive_card(Card(Suit.HEARTS, Rank.KING))

        # Bob has a Straight
        player2.receive_card(Card(Suit.CLUBS, Rank.NINE))
        player2.receive_card(Card(Suit.SPADES, Rank.TEN))

        community_cards = [
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.SPADES, Rank.NINE),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.SEVEN)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Full House vs. Straight test failed")

    # test case for Three of a Kind vs. Two Pair
    def test_three_of_a_kind_vs_two_pair(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has Three of a Kind
        player1.receive_card(Card(Suit.HEARTS, Rank.QUEEN))
        player1.receive_card(Card(Suit.DIAMONDS, Rank.QUEEN))

        # Bob has Two Pair
        player2.receive_card(Card(Suit.SPADES, Rank.KING))
        player2.receive_card(Card(Suit.CLUBS, Rank.KING))

        community_cards = [
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.DIAMONDS, Rank.TEN),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.CLUBS, Rank.TWO),
            Card(Suit.SPADES, Rank.THREE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Three of a Kind vs. Two Pair test failed")

    # test case for Full House vs. Flush
    def test_full_house_vs_flush(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Full House
        player1.receive_card(Card(Suit.SPADES, Rank.JACK))
        player1.receive_card(Card(Suit.HEARTS, Rank.JACK))

        # Bob has a Flush
        player2.receive_card(Card(Suit.CLUBS, Rank.NINE))
        player2.receive_card(Card(Suit.CLUBS, Rank.THREE))

        community_cards = [
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.SPADES, Rank.NINE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Full House vs. Flush test failed")

    # test case for Straight vs. Three of a Kind
    def test_straight_vs_three_of_a_kind(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Straight
        player1.receive_card(Card(Suit.SPADES, Rank.FIVE))
        player1.receive_card(Card(Suit.CLUBS, Rank.SIX))

        # Bob has Three of a Kind
        player2.receive_card(Card(Suit.HEARTS, Rank.FOUR))
        player2.receive_card(Card(Suit.SPADES, Rank.FOUR))

        community_cards = [
            Card(Suit.DIAMONDS, Rank.THREE),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.EIGHT)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Straight vs. Three of a Kind test failed")

    # test case for One Pair vs. High Card
    def test_one_pair_vs_high_card(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has One Pair
        player1.receive_card(Card(Suit.SPADES, Rank.TEN))
        player1.receive_card(Card(Suit.DIAMONDS, Rank.TEN))

        # Bob has only a High Card
        player2.receive_card(Card(Suit.CLUBS, Rank.ACE))
        player2.receive_card(Card(Suit.SPADES, Rank.KING))

        community_cards = [
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.DIAMONDS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.NINE),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "One Pair vs. High Card test failed")

    # test case for Split Pot with Two Pair
    def test_two_pair_split_pot(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Both Alice and Bob have the same Two Pair
        player1.receive_card(Card(Suit.SPADES, Rank.JACK))
        player1.receive_card(Card(Suit.HEARTS, Rank.FIVE))

        player2.receive_card(Card(Suit.CLUBS, Rank.JACK))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.FIVE))

        community_cards = [
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.HEARTS, Rank.THREE),
            Card(Suit.SPADES, Rank.FOUR),
            Card(Suit.CLUBS, Rank.SIX)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"}, "Two Pair split pot test failed")

    # test case for Straight vs. Two Pair
    def test_straight_vs_two_pair(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice has a Straight
        player1.receive_card(Card(Suit.HEARTS, Rank.SIX))
        player1.receive_card(Card(Suit.SPADES, Rank.SEVEN))

        # Bob has Two Pair
        player2.receive_card(Card(Suit.CLUBS, Rank.NINE))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.NINE))

        community_cards = [
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.FOUR),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.TEN)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"], "Straight vs. Two Pair test failed")

    # test case for Split Pot with Low Straight (Ace through Five)
    def test_low_straight_split_pot(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Alice and Bob both have a low straight (Ace to Five)
        player1.receive_card(Card(Suit.SPADES, Rank.ACE))
        player1.receive_card(Card(Suit.HEARTS, Rank.TWO))

        player2.receive_card(Card(Suit.DIAMONDS, Rank.ACE))
        player2.receive_card(Card(Suit.CLUBS, Rank.TWO))

        community_cards = [
            Card(Suit.SPADES, Rank.THREE),
            Card(Suit.HEARTS, Rank.FOUR),
            Card(Suit.DIAMONDS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.HEARTS, Rank.NINE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"}, "Low Straight split pot test failed")

    # test case for Four-Way Split Pot with Straight on the Board
    def test_four_way_split_pot_with_straight(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Each player has cards that do not improve upon the board straight
        player1.receive_card(Card(Suit.SPADES, Rank.TWO))
        player1.receive_card(Card(Suit.HEARTS, Rank.THREE))

        player2.receive_card(Card(Suit.CLUBS, Rank.TWO))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.THREE))

        player3.receive_card(Card(Suit.SPADES, Rank.FOUR))
        player3.receive_card(Card(Suit.CLUBS, Rank.FOUR))

        player4.receive_card(Card(Suit.CLUBS, Rank.SIX))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.SIX))

        # Community cards form a straight from Five to Nine
        community_cards = [
            Card(Suit.SPADES, Rank.FIVE),
            Card(Suit.HEARTS, Rank.SIX),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.NINE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob", "Charlie", "Diana"},
                         "Four-way split pot with straight test failed")

    def test_one_pair_single_winner(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Player 1 has the highest pair
        player1.receive_card(Card(Suit.SPADES, Rank.ACE))
        player1.receive_card(Card(Suit.HEARTS, Rank.KING))

        player2.receive_card(Card(Suit.CLUBS, Rank.KING))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.QUEEN))

        player3.receive_card(Card(Suit.SPADES, Rank.JACK))
        player3.receive_card(Card(Suit.CLUBS, Rank.TEN))

        player4.receive_card(Card(Suit.CLUBS, Rank.NINE))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.EIGHT))

        # Community cards
        community_cards = [
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.JACK),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.DIAMONDS, Rank.FIVE),
            Card(Suit.HEARTS, Rank.TWO)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice"],
                         "Single winner test failed")

    def test_one_pair_two_winners(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Players 1 and 2 both have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.NINE))
        player1.receive_card(Card(Suit.HEARTS, Rank.THREE))

        player2.receive_card(Card(Suit.CLUBS, Rank.NINE))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.FOUR))

        player3.receive_card(Card(Suit.SPADES, Rank.FIVE))
        player3.receive_card(Card(Suit.CLUBS, Rank.TWO))

        player4.receive_card(Card(Suit.CLUBS, Rank.SIX))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.TWO))

        # Community cards
        community_cards = [
            Card(Suit.HEARTS, Rank.NINE),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.DIAMONDS, Rank.JACK),
            Card(Suit.HEARTS, Rank.QUEEN)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"},
                         "Two winners test failed")

    def test_one_pair_three_winners(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Players 1, 2, and 3 all have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.TEN))
        player1.receive_card(Card(Suit.HEARTS, Rank.FOUR))

        player2.receive_card(Card(Suit.CLUBS, Rank.TEN))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.TWO))

        player3.receive_card(Card(Suit.SPADES, Rank.TEN))
        player3.receive_card(Card(Suit.CLUBS, Rank.THREE))

        player4.receive_card(Card(Suit.CLUBS, Rank.SIX))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.EIGHT))

        # Community cards
        community_cards = [
            Card(Suit.SPADES, Rank.NINE),
            Card(Suit.HEARTS, Rank.TEN),
            Card(Suit.CLUBS, Rank.JACK),
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob", "Charlie"},
                         "Three winners test failed")

    def test_one_pair_kicker_decides(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Player 1 and Player 2 have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.QUEEN))
        player1.receive_card(Card(Suit.HEARTS, Rank.ACE))

        player2.receive_card(Card(Suit.CLUBS, Rank.QUEEN))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.ACE))

        player3.receive_card(Card(Suit.SPADES, Rank.ACE))
        player3.receive_card(Card(Suit.CLUBS, Rank.FIVE))

        player4.receive_card(Card(Suit.CLUBS, Rank.TWO))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.SIX))

        # Community cards
        community_cards = [
            Card(Suit.SPADES, Rank.TWO),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.THREE),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.HEARTS, Rank.EIGHT)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])

        print(player1.get_best_hand(community_cards))
        print(player2.get_best_hand(community_cards))

        winners = analyzer.analyze_winners()

        print(winners)

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(winner_names, ["Alice", "Bob"],
                         "Kicker decides winner test failed")

    def test_one_pair_kicker_two_players(self):
        player1 = Player("Alice")
        player2 = Player("Bob")
        player3 = Player("Charlie")
        player4 = Player("Diana")

        # Players 1 and 2 both have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.SEVEN))
        player1.receive_card(Card(Suit.HEARTS, Rank.TEN))

        player2.receive_card(Card(Suit.CLUBS, Rank.SEVEN))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.TEN))

        player3.receive_card(Card(Suit.SPADES, Rank.ACE))
        player3.receive_card(Card(Suit.CLUBS, Rank.TWO))

        player4.receive_card(Card(Suit.CLUBS, Rank.THREE))
        player4.receive_card(Card(Suit.DIAMONDS, Rank.FOUR))

        # Community cards
        community_cards = [
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.HEARTS, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.NINE),
            Card(Suit.HEARTS, Rank.FIVE)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
            (player3.name, player3.get_best_hand(community_cards)[1]),
            (player4.name, player4.get_best_hand(community_cards)[1])
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"},
                         "Kicker deciding two players test failed")

    def test_flush_split(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Players 1 and 2 both have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.TWO))
        player1.receive_card(Card(Suit.SPADES, Rank.FIVE))

        player2.receive_card(Card(Suit.SPADES, Rank.FOUR))
        player2.receive_card(Card(Suit.SPADES, Rank.THREE))


        # Community cards
        community_cards = [
            Card(Suit.SPADES, Rank.TEN),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.SPADES, Rank.EIGHT),
            Card(Suit.SPADES, Rank.NINE),
            Card(Suit.SPADES, Rank.KING)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"},
                         "Kicker deciding two players test failed")

    def test_high_split(self):
        player1 = Player("Alice")
        player2 = Player("Bob")

        # Players 1 and 2 both have the same pair
        player1.receive_card(Card(Suit.SPADES, Rank.TWO))
        player1.receive_card(Card(Suit.SPADES, Rank.EIGHT))

        player2.receive_card(Card(Suit.SPADES, Rank.FOUR))
        player2.receive_card(Card(Suit.DIAMONDS, Rank.EIGHT))


        # Community cards
        community_cards = [
            Card(Suit.CLUBS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SIX),
            Card(Suit.SPADES, Rank.NINE),
            Card(Suit.HEARTS, Rank.KING)
        ]

        analyzer = WinnerAnalyzer([
            (player1.name, player1.get_best_hand(community_cards)[1]),
            (player2.name, player2.get_best_hand(community_cards)[1]),
        ])
        winners = analyzer.analyze_winners()

        # Extract winner names
        winner_names = [winner[0] for winner in winners]
        self.assertEqual(set(winner_names), {"Alice", "Bob"},
                         "Kicker deciding two players test failed")

if __name__ == "__main__":
    unittest.main()