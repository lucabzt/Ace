from collections import Counter
from itertools import \
    combinations  # Importiert die Funktion combinations, um alle möglichen 5-Karten-Kombinationen zu erzeugen

from card import Rank  # Importiert die Klasse Rank aus dem Modul card
from hand_rankings import (  # Importiert Handbewertungsmethoden aus dem Modul hand_rankings
    is_flush, is_straight, is_four_of_a_kind, is_full_house,
    is_three_of_a_kind, is_two_pair, is_one_pair, high_card
)


# Klasse zur Analyse einer Pokerhand
class PokerHandAnalyzer:
    def __init__(self, cards):
        """
        Initialisiert die PokerHandAnalyzer-Klasse mit genau 7 Karten.
        Wirft einen Fehler, wenn nicht genau 7 Karten übergeben werden.
        Wirft einen Fehler, wenn exakte Karte zwei mal vorkommt.
        """
        if self.has_duplicate_cards(cards):  # Use the helper method to check for duplicates
            duplicate_cards = self.get_duplicate_cards(cards)
            raise ValueError(f"Duplicate cards found: {', '.join(map(str, duplicate_cards))}")

        if len(cards) != 7:  # Es müssen genau 7 Karten sein, um die beste Hand zu analysieren
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
            hand_type, hand = self.evaluate_hand(combination)  # Bewertet jede 5-Karten-Hand
            # Aktualisiert die beste Hand, wenn der aktuelle Handtyp besser ist
            if best_hand_type is None or hand_type < best_hand_type:
                best_hand_type = hand_type  # Speichert den neuen besten Handtyp
                best_hand = hand  # Speichert die neue beste Hand

        return best_hand  # Gibt die beste Hand zurück

    # Methode zur Bewertung einer einzelnen 5-Karten-Hand
    def evaluate_hand(self, hand):
        """
        Bewertet eine gegebene 5-Karten-Hand und bestimmt deren Typ.
        Gibt ein Tupel zurück, bestehend aus dem Handrang (Integer, wobei niedrigere Zahlen besser sind)
        und der Hand selbst (Textbeschreibung).
        """
        # Überprüft auf Royal Flush (höchster Straight Flush mit 10-A)
        if is_flush(hand) and is_straight(hand) and all(
                rank in [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE] for rank in
                [card.rank for card in hand]):
            return (1, "Royal Flush")  # Beste Hand: Royal Flush

        # Überprüft auf Straight Flush (alle Karten in Folge und gleiche Farbe)
        elif is_flush(hand) and is_straight(hand):
            return (2, "Straight Flush")  # Zweitbeste Hand: Straight Flush

        # Überprüft auf Four of a Kind (Vierling)
        elif is_four_of_a_kind(hand):
            return (3, "Four of a Kind")  # Vierling

        # Überprüft auf Full House (Drei gleiche Karten + zwei gleiche Karten)
        elif is_full_house(hand):
            return (4, "Full House")  # Full House

        # Überprüft auf Flush (alle Karten gleiche Farbe)
        elif is_flush(hand):
            return (5, "Flush")  # Flush

        # Überprüft auf Straight (alle Karten in Folge, aber unterschiedliche Farben)
        elif is_straight(hand):
            return (6, "Straight")  # Straße

        # Überprüft auf Three of a Kind (Drilling)
        elif is_three_of_a_kind(hand):
            return (7, "Three of a Kind")  # Drilling

        # Überprüft auf Two Pair (zwei Paare)
        elif is_two_pair(hand):
            return (8, "Two Pair")  # Zwei Paare

        # Überprüft auf One Pair (ein Paar)
        elif is_one_pair(hand):
            return (9, "One Pair")  # Ein Paar

        # Keine Kombination gefunden: höchste Karte
        else:
            return (10, f"High Card: {high_card(hand)}")  # Höchste Karte (High Card)

    def has_duplicate_cards(self, cards):
        """
        Überprüft, ob in den gespeicherten Karten doppelte Karten vorhanden sind.
        Gibt True zurück, wenn eine Karte doppelt vorkommt, andernfalls False.
        """
        unique_cards = set(cards)  # Create a set from the list of cards
        # If the length of unique cards is less than the original, duplicates exist
        return len(unique_cards) < len(cards)

    def get_duplicate_cards(self, cards):
        """
        Gibt eine Liste der doppelten Karten zurück.
        """
        counter = Counter(cards)
        return [card for card, count in counter.items() if count > 1]