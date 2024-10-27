from itertools import combinations

from Hand_Analysis.card import Rank, Card
from Hand_Analysis.hand_analyzer import PokerHandAnalyzer
from Hand_Analysis.hand_rankings import rank_value, is_flush, is_straight, is_four_of_a_kind, is_full_house, \
    is_three_of_a_kind, is_two_pair, is_one_pair, high_card


class WinnerAnalyzer:
    def __init__(self, players):
        self.players = players  # List of tuples (player_name, player_cards)

    def analyze_winners(self):
        """
        Analyzes all players' hands and determines the winner(s) based on the best hand.
        Handles tie situations by returning all players with the best hand.

        :return: A list of tuples containing player names and their best hands.
        """
        winners = []
        best_hand = None
        best_hand_type = None
        best_player_name = None

        # Loop through each player in the array
        for player_name, player_cards in self.players:
            hand_type, attr = self.evaluate_hand(player_cards)

            if best_hand_type is None or hand_type < best_hand_type:
                best_hand_type = hand_type
                best_hand = (player_cards, attr)

                winners.clear()
                winners.append((player_name, best_hand_type, best_hand))

            elif hand_type == best_hand_type:
                best_combination, best_attr = best_hand  # Unpack properly

                temp = best_hand
                best_hand, split_pot = self.tie_breaker(hand_type, player_cards, attr, best_attr, best_hand)

                if split_pot:
                    winners.append((player_name, best_hand_type, best_hand))
                elif temp != best_hand:
                    best_hand_type = hand_type
                    best_hand = (player_cards, attr)

                    winners.clear()
                    winners.append((player_name, best_hand_type, best_hand))

        winners = self.translate_winner_hands(winners)

        return winners

    # Methode zur Bewertung einer einzelnen 5-Karten-Hand
    def evaluate_hand(self, hand):
        """
        Bewertet eine gegebene 5-Karten-Hand und bestimmt deren Typ.
        Gibt ein Tupel zurück, bestehend aus dem Handrang (Integer, wobei niedrigere Zahlen besser sind)
        und der höchsten Karte zur Tie-Breaking.
        """
        # Überprüft auf Royal Flush (höchster Straight Flush mit 10-A)
        flush, flush_high = is_flush(hand)

        straight, straight_high = is_straight(hand)

        four_of_a_kind, quad_rank, quad_kicker = is_four_of_a_kind(hand)

        full_house, fh_three_rank, fh_pair_rank = is_full_house(hand)

        three_of_a_kind, three_rank, three_kicker_1_rank, three_kicker_2_rank = is_three_of_a_kind(hand)

        two_pair, high_pair, low_pair, two_pair_kicker = is_two_pair(hand)

        one_pair, pair_rank, kicker_1_rank, kicker_2_rank, kicker_3_rank = is_one_pair(hand)

        if flush and straight and straight_high.rank == Rank.ACE:
            return 1, [straight_high]  # Beste Hand: Royal Flush

        # Überprüft auf Straight Flush (alle Karten in Folge und gleiche Farbe)
        elif flush and straight:
            return 2, [straight_high]  # Straight Flush mit höchster Karte

        # Überprüft auf Four of a Kind (Vierling)
        if four_of_a_kind:
            return 3, [quad_rank, quad_kicker]  # Four of a Kind mit Kicker

        # Überprüft auf Full House (Drei gleiche Karten + zwei gleiche Karten)
        if full_house:
            return 4, [fh_three_rank, fh_pair_rank]  # Full House, Drilling gefolgt von Paar

        # Überprüft auf Flush (alle Karten gleiche Farbe)
        if flush:
            return 5, [flush_high]  # Flush mit höchster Karte

        # Überprüft auf Straight (alle Karten in Folge, aber unterschiedliche Farben)
        if straight:
            return 6, [straight_high]  # Straße mit höchster Karte

        # Überprüft auf Three of a Kind (Drilling)
        if three_of_a_kind:
            return 7, [three_rank, three_kicker_1_rank, three_kicker_2_rank]  # Drilling gefolgt von den besten Kickern

        # Überprüft auf Two Pair (zwei Paare)
        if two_pair:
            return 8, [high_pair, low_pair, two_pair_kicker]  # Zwei Paare mit Kicker

        # Überprüft auf One Pair (ein Paar)
        if one_pair:
            return 9, [pair_rank, kicker_1_rank, kicker_2_rank, kicker_3_rank]  # Paar mit Kickern

        # Keine Kombination gefunden: höchste Karte
        high = high_card(hand)
        return 10, [high]  # Höchste Karte (High Card)

    def tie_breaker(self, hand_type, challenger_combination, challenger_attr, old_best_attr, old_best_hand):

        best_hand = old_best_hand
        # Differentiating tie-breaking logic based on hand type
        if hand_type in [1, 2, 6]:  # Royal Flush, Straight Flush, Straight
            split_pot = False

            challenger_high_card = challenger_attr[0]
            old_high_card = old_best_attr[0]
            # Compare the highest card in the straight
            if self.compare_high_cards(challenger_high_card, old_high_card) > 0:
                best_hand = (challenger_combination, challenger_attr)
            elif self.compare_high_cards(challenger_high_card, old_high_card) == 0:
                split_pot = True
                best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 3:  # Four of a Kind
            split_pot = False

            challenger_rank = challenger_attr[0]
            old_rank = old_best_attr[0]

            challenger_kicker = challenger_attr[1]
            old_kicker = old_best_attr[1]
            # Compare the rank of the Four of a Kind, and then the kicker
            if rank_value(challenger_rank.rank) > rank_value(old_rank.rank):
                best_hand = (challenger_combination, challenger_attr)
            elif rank_value(challenger_rank.rank) == rank_value(old_rank.rank):
                if self.compare_high_cards(challenger_kicker, old_kicker) > 0:
                    best_hand = (challenger_combination, challenger_attr)
                elif self.compare_high_cards(challenger_kicker, old_kicker) == 0:
                    split_pot = True
                    best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 4:  # Full House
            # Compare the three of a kind rank, and if equal, compare the pair
            split_pot = False

            challenger_three_of_a_kind_rank = challenger_attr[0]
            old_three_of_a_kind_rank = old_best_attr[0]

            challenger_pair_rank = challenger_attr[1]
            old_pair_rank = old_best_attr[1]

            if rank_value(challenger_three_of_a_kind_rank) > rank_value(old_three_of_a_kind_rank):
                best_hand = (challenger_combination, challenger_attr)
            elif rank_value(challenger_three_of_a_kind_rank) == rank_value(old_three_of_a_kind_rank):
                if rank_value(challenger_pair_rank) > rank_value(old_pair_rank):
                    best_hand = (challenger_combination, challenger_attr)
                elif rank_value(challenger_pair_rank) == rank_value(old_pair_rank):
                    split_pot = True
                    best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 5:  # Flush
            # Compare high cards in Flush
            split_pot = False

            challenger_high_card = challenger_attr[0]
            old_high_card = old_best_attr[0]

            if self.compare_high_cards(challenger_high_card, old_high_card) > 0:
                best_hand = (challenger_combination, challenger_attr)
            elif self.compare_high_cards(challenger_high_card, old_high_card) == 0:
                split_pot = True
                best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 7:  # Three of a Kind

            split_pot = False

            challenger_three_of_a_kind_rank = challenger_attr[0]
            old_three_of_a_kind_rank = old_best_attr[0]

            # Assume kickers are provided as individual attributes for each kicker rank
            challenger_kicker_1 = challenger_attr[1]
            challenger_kicker_2 = challenger_attr[2]

            old_kicker_1 = old_best_attr[1]
            old_kicker_2 = old_best_attr[2]

            if rank_value(challenger_three_of_a_kind_rank) > rank_value(old_three_of_a_kind_rank):
                best_hand = (challenger_combination, challenger_attr)
            elif rank_value(challenger_three_of_a_kind_rank) == rank_value(old_three_of_a_kind_rank):
                # Compare each kicker directly
                if challenger_kicker_1 > old_kicker_1:
                    best_hand = (challenger_combination, challenger_attr)
                elif challenger_kicker_1 == old_kicker_1:
                    if challenger_kicker_2 > old_kicker_2:
                        best_hand = (challenger_combination, challenger_attr)
                    elif challenger_kicker_2 == old_kicker_2:
                        split_pot = True
                        best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 8:  # Two Pair
            split_pot = False

            challenger_high_pair = challenger_attr[0]
            old_high_pair = old_best_attr[0]

            challenger_low_pair = challenger_attr[1]
            old_low_pair = old_best_attr[1]

            challenger_kicker = challenger_attr[2]
            old_kicker = old_best_attr[2]

            # Compare the higher pair first, then the lower pair, and finally the kicker
            if rank_value(challenger_high_pair) > rank_value(old_high_pair):
                best_hand = (challenger_combination, challenger_attr)
            elif rank_value(challenger_high_pair) == rank_value(old_high_pair):
                if rank_value(challenger_low_pair) > rank_value(old_low_pair):
                    best_hand = (challenger_combination, challenger_attr)
                elif rank_value(challenger_low_pair) == rank_value(old_low_pair):
                    if rank_value(challenger_kicker.rank) > rank_value(old_kicker.rank):
                        best_hand = (challenger_combination, challenger_attr)
                    elif rank_value(challenger_kicker.rank) == rank_value(old_kicker.rank):
                        split_pot = True
                        best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

        elif hand_type == 9:  # One Pair
            split_pot = False

            challenger_pair = challenger_attr[0]
            old_pair = old_best_attr[0]

            # Assume kickers are provided as individual attributes for each kicker rank
            challenger_kicker_1 = challenger_attr[1]
            challenger_kicker_2 = challenger_attr[2]
            challenger_kicker_3 = challenger_attr[3]

            old_kicker_1 = old_best_attr[1]
            old_kicker_2 = old_best_attr[2]
            old_kicker_3 = old_best_attr[3]

            # Compare the pair ranks first, then kickers if pairs are tied
            if rank_value(challenger_pair) > rank_value(old_pair):
                best_hand = (challenger_combination, challenger_attr)
            elif rank_value(challenger_pair) == rank_value(old_pair):
                # Compare each kicker directly
                if challenger_kicker_1 > old_kicker_1:
                    best_hand = (challenger_combination, challenger_attr)
                elif challenger_kicker_1 == old_kicker_1:
                    if challenger_kicker_2 > old_kicker_2:
                        best_hand = (challenger_combination, challenger_attr)
                    elif challenger_kicker_2 == old_kicker_2:
                        if challenger_kicker_3 > old_kicker_3:
                            best_hand = (challenger_combination, challenger_attr)
                        elif challenger_kicker_3 == old_kicker_3:
                            split_pot = True
                            best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot


        elif hand_type == 10:  # High Card
            split_pot = False
            challenger_high_card = challenger_attr[0]
            old_high_card = old_best_attr[0]

            # Compare the highest card in the straight
            if self.compare_high_cards(challenger_high_card, old_high_card) > 0:
                best_hand = (challenger_combination, challenger_attr)

            return best_hand, split_pot

    def compare_high_cards(self, high_cards1, high_cards2):
        """
        Vergleicht zwei Listen von High Cards und bestimmt, welche Liste stärker ist.
        Gibt 1 zurück, wenn high_cards1 stärker ist, -1, wenn high_cards2 stärker ist, und 0 bei Gleichheit.
        """

        # Ensure that both high_cards1 and high_cards2 are lists
        if not isinstance(high_cards1, list):
            high_cards1 = [high_cards1]  # Convert to a list if it's a single Card
        if not isinstance(high_cards2, list):
            high_cards2 = [high_cards2]  # Convert to a list if it's a single Card

        # Iterate over the pairs of high cards
        for card1, card2 in zip(high_cards1, high_cards2):
            if rank_value(card1.rank) > rank_value(card2.rank):
                return 1
            elif rank_value(card1.rank) < rank_value(card2.rank):
                return -1

        # If all compared cards are equal, return 0
        return 0  # Hände sind gleich stark

    def has_duplicate_cards(self, cards):
        """
        Überprüft, ob in den gespeicherten Karten doppelte Karten vorhanden sind.
        Gibt True zurück, wenn eine Karte doppelt vorkommt, andernfalls False.
        """
        unique_cards = set(cards)
        return len(unique_cards) < len(cards)

    # Function to modify the best_hand_type in winners array to descriptive names
    def translate_winner_hands(self, winners):

        # Mapping integer values to poker hands
        best_hand_dict = {
            1: "Royal Flush",
            2: "Straight Flush",
            3: "Four of a Kind",
            4: "Full House",
            5: "Flush",
            6: "Straight",
            7: "Three of a Kind",
            8: "Two Pair",
            9: "One Pair",
            10: "High Card"
        }

        updated_winners = []
        for winner in winners:
            winner_id = winner[0]
            hand_type_num = winner[1]
            hand_name = best_hand_dict.get(hand_type_num, "Unknown Hand")
            # Create a new tuple with the updated hand name
            updated_winner = (winner_id, hand_name, *winner[2:])
            updated_winners.append(updated_winner)
        return updated_winners
