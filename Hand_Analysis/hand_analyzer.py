from collections import Counter
from itertools import combinations

from Hand_Analysis.card import Rank
from Hand_Analysis.hand_rankings import rank_value, high_card, is_one_pair, is_two_pair, is_three_of_a_kind, \
    is_full_house, is_four_of_a_kind, is_straight, is_flush


class PokerHandAnalyzer:
    def __init__(self, cards):
        """
        Initialisiert die PokerHandAnalyzer-Klasse mit genau 7 Karten.
        """
        if self.has_duplicate_cards(cards):  # Check for duplicate cards
            duplicate_cards = self.get_duplicate_cards(cards)
            raise ValueError(f"Duplicate cards found: {', '.join(map(str, duplicate_cards))}")

        if len(cards) != 7:  # Es müssen genau 7 Karten sein
            raise ValueError("Exactly 7 cards are required to analyze.")  # Fehler bei falscher Kartenanzahl
        self.cards = cards  # Speichert die Karten

    # Methode, um die beste 5-Karten-Hand aus den 7 Karten zu ermitteln
    def get_best_hand(self):
        """
        Ermittelt die beste 5-Karten-Hand aus den 7 gegebenen Karten.
        Gibt die beste Hand zurück.
        """
        best_hand = None  # Variable für die beste Hand
        best_hand_type = None  # Variable für den besten Handtyp

        # Erzeugt alle möglichen 5-Karten-Kombinationen aus den 7 Karten
        for combination in combinations(self.cards, 5):  # Kombiniert die 7 Karten in 5-Karten-Hände
            hand_type, high_cards = self.evaluate_hand(combination)  # Bewertet jede 5-Karten-Hand
            # Aktualisiert die beste Hand, wenn der aktuelle Handtyp besser ist
            if best_hand_type is None or hand_type < best_hand_type:
                best_hand_type = hand_type  # Speichert den neuen besten Handtyp
                best_hand = (combination, high_cards)  # Speichert die neue beste Hand und relevante Karten
            # If hands have the same rank, compare high cards to break the tie
            elif hand_type == best_hand_type:
                _, current_high_cards = best_hand

                # Differentiating tie-breaking logic based on hand type
                if hand_type in [1, 2, 6]:  # Royal Flush, Straight Flush, Straight
                    # Compare the highest card in the straight
                    if self.compare_high_cards(high_cards, current_high_cards) > 0:
                        best_hand = (combination, high_cards)

                elif hand_type == 3:  # Four of a Kind
                    # Compare the rank of the Four of a Kind, and then the kicker
                    if rank_value(high_cards[0].rank) > rank_value(current_high_cards[0].rank):
                        best_hand = (combination, high_cards)
                    elif rank_value(high_cards[0].rank) == rank_value(current_high_cards[0].rank):
                        if rank_value(high_cards[1].rank) > rank_value(current_high_cards[1].rank):
                            best_hand = (combination, high_cards)

                elif hand_type == 4:  # Full House
                    # Compare the three of a kind rank, and if equal, compare the pair
                    if rank_value(high_cards[0].rank) > rank_value(current_high_cards[0].rank):
                        best_hand = (combination, high_cards)
                    elif rank_value(high_cards[0].rank) == rank_value(current_high_cards[0].rank):
                        if rank_value(high_cards[1].rank) > rank_value(current_high_cards[1].rank):
                            best_hand = (combination, high_cards)

                elif hand_type == 5:  # Flush
                    # Compare high cards in Flush
                    if self.compare_high_cards(high_cards, current_high_cards) > 0:
                        best_hand = (combination, high_cards)

                elif hand_type == 7:  # Three of a Kind
                    # Compare the three of a kind rank, and then the kickers
                    if rank_value(high_cards[0].rank) > rank_value(current_high_cards[0].rank):
                        best_hand = (combination, high_cards)
                    elif rank_value(high_cards[0].rank) == rank_value(current_high_cards[0].rank):
                        if self.compare_high_cards(high_cards[1:], current_high_cards[1:]) > 0:
                            best_hand = (combination, high_cards)

                elif hand_type == 8:  # Two Pair
                    # Compare the higher pair first, then the lower pair, and finally the kicker
                    if rank_value(high_cards[0].rank) > rank_value(current_high_cards[0].rank):
                        best_hand = (combination, high_cards)
                    elif rank_value(high_cards[0].rank) == rank_value(current_high_cards[0].rank):
                        if rank_value(high_cards[1].rank) > rank_value(current_high_cards[1].rank):
                            best_hand = (combination, high_cards)
                        elif rank_value(high_cards[1].rank) == rank_value(current_high_cards[1].rank):
                            if rank_value(high_cards[2].rank) > rank_value(current_high_cards[2].rank):
                                best_hand = (combination, high_cards)

                elif hand_type == 9:  # One Pair
                    # Compare the pair, and then the kickers
                    if rank_value(high_cards[0].rank) > rank_value(current_high_cards[0].rank):
                        best_hand = (combination, high_cards)
                    elif rank_value(high_cards[0].rank) == rank_value(current_high_cards[0].rank):
                        if self.compare_high_cards(high_cards[1:], current_high_cards[1:]) > 0:
                            best_hand = (combination, high_cards)

                elif hand_type == 10:  # High Card
                    # Simply compare the high cards in order
                    if self.compare_high_cards(high_cards, current_high_cards) > 0:
                        best_hand = (combination, high_cards)

        return best_hand[0]  # Gibt die beste Hand (5 Karten) zurück

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

        if flush and straight and straight_high.rank == Rank.ACE:
            return 1, [straight_high]  # Beste Hand: Royal Flush

        # Überprüft auf Straight Flush (alle Karten in Folge und gleiche Farbe)
        elif flush and straight:
            return 2, [straight_high]  # Straight Flush mit höchster Karte

        # Überprüft auf Four of a Kind (Vierling)
        four_of_a_kind, quad_rank, kicker = is_four_of_a_kind(hand)
        if four_of_a_kind:
            return 3, [quad_rank, kicker]  # Four of a Kind mit Kicker

        # Überprüft auf Full House (Drei gleiche Karten + zwei gleiche Karten)
        full_house, three_rank, pair_rank = is_full_house(hand)
        if full_house:
            return 4, [three_rank, pair_rank]  # Full House, Drilling gefolgt von Paar

        # Überprüft auf Flush (alle Karten gleiche Farbe)
        if flush:
            return 5, [flush_high]  # Flush mit höchster Karte

        # Überprüft auf Straight (alle Karten in Folge, aber unterschiedliche Farben)
        if straight:
            return 6, [straight_high]  # Straße mit höchster Karte

        # Überprüft auf Three of a Kind (Drilling)
        three_of_a_kind, three_rank, kickers = is_three_of_a_kind(hand)
        if three_of_a_kind:
            return 7, [three_rank] + kickers  # Drilling gefolgt von den besten Kickern

        # Überprüft auf Two Pair (zwei Paare)
        two_pair, high_pair, low_pair, kicker = is_two_pair(hand)
        if two_pair:
            return 8, [high_pair, low_pair, kicker]  # Zwei Paare mit Kicker

        # Überprüft auf One Pair (ein Paar)
        one_pair, pair_rank, kickers = is_one_pair(hand)
        if one_pair:
            return 9, [pair_rank] + kickers  # Paar mit Kickern

        # Keine Kombination gefunden: höchste Karte
        high = high_card(hand)
        return 10, [high]  # Höchste Karte (High Card)

    def compare_high_cards(self, high_cards1, high_cards2):
        """
        Vergleicht zwei Listen von High Cards und bestimmt, welche Liste stärker ist.
        Gibt 1 zurück, wenn high_cards1 stärker ist, -1, wenn high_cards2 stärker ist, und 0 bei Gleichheit.
        """
        for card1, card2 in zip(high_cards1, high_cards2):
            if rank_value(card1.rank) > rank_value(card2.rank):
                return 1
            elif rank_value(card1.rank) < rank_value(card2.rank):
                return -1
        return 0  # Hände sind gleich stark

    def has_duplicate_cards(self, cards):
        """
        Überprüft, ob in den gespeicherten Karten doppelte Karten vorhanden sind.
        Gibt True zurück, wenn eine Karte doppelt vorkommt, andernfalls False.
        """
        unique_cards = set(cards)
        return len(unique_cards) < len(cards)

    def get_duplicate_cards(self, cards):
        """
        Gibt eine Liste der doppelten Karten zurück.
        """
        counter = Counter(cards)
        return [card for card, count in counter.items() if count > 1]
