from itertools import combinations

from hand_analysis.utils import evaluate_hand, has_duplicate_cards, get_duplicate_cards, \
    tie_breaker


class PokerHandAnalyzer:
    def __init__(self, cards):
        """
        Initialisiert die PokerHandAnalyzer-Klasse mit genau 7 Karten.
        """
        if has_duplicate_cards(cards):  # Check for duplicate cards
            duplicate_cards = get_duplicate_cards(cards)
            raise ValueError(f"Duplicate cards found: {', '.join(map(str, duplicate_cards))}")

        if len(cards) != 7:  # Es müssen genau 7 Karten sein
            raise ValueError("Exactly 7 cards are required to analyze.")  # Fehler bei falscher Kartenanzahl

        self.cards = cards  # Speichert die Karten

    # Methode, um die beste 5-Karten-Hand aus den 7 Karten zu ermitteln
    def get_best_hand(self):
        """
        Ermittelt die beste 5-Karten-Hand aus den 7 gegebenen Karten und gibt eine strukturierte Ausgabe zurück,
        die den Handtyp und wichtige Informationen zur Hand (wie Kickers) enthält.
        """
        best_hand = None
        best_hand_type = None

        for combination in combinations(self.cards, 5):
            hand_type, attr = evaluate_hand(combination)

            if best_hand_type is None or hand_type < best_hand_type:
                best_hand_type = hand_type
                best_hand = (combination, attr)
            elif hand_type == best_hand_type:
                best_combination, best_attr = best_hand  # Unpack properly
                best_hand, _ = tie_breaker(hand_type, combination, attr, best_attr, best_hand)

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

        return best_hand_dict.get(best_hand_type), best_hand[0]
