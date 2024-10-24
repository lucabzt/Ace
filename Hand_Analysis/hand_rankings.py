from collections import Counter  # Importiert Counter aus collections, um Häufigkeiten von Kartenrängen zu zählen

from Hand_Analysis.card import Card, Suit, Rank # Importiert die Klassen Card und Rank aus einem externen Modul card


# Hilfsfunktion, um die Anzahl der verschiedenen Ränge in einer Hand zu ermitteln
def get_rank_counts(hand):
    """
    Gibt ein Counter-Objekt zurück, das die Häufigkeit der Ränge in der Hand darstellt.
    Die Hand ist eine Liste von Card-Objekten.
    """
    ranks = [card.rank for card in hand]  # Extrahiert die Ränge aus der Hand
    return Counter(ranks)  # Zählt, wie oft jeder Rang vorkommt


# Hilfsfunktion, um den Wert eines Rangs zu ermitteln

def rank_value(rank):
    rank_values = {
        Rank.TWO: 2,
        Rank.THREE: 3,
        Rank.FOUR: 4,
        Rank.FIVE: 5,
        Rank.SIX: 6,
        Rank.SEVEN: 7,
        Rank.EIGHT: 8,
        Rank.NINE: 9,
        Rank.TEN: 10,
        Rank.JACK: 11,
        Rank.QUEEN: 12,
        Rank.KING: 13,
        Rank.ACE: 14
    }

    """
    Gibt den numerischen Wert eines Rangs zurück, um Kartenwerte zu vergleichen.
    Zum Beispiel: TWO = 2, THREE = 3, ..., ACE = 14.
    """
    return rank_values[rank]
    # Gibt den entsprechenden Wert eines Rangs zurück


# Prüft, ob alle Karten in der Hand die gleiche Farbe (Suit) haben
def is_flush(hand):
    """
    Überprüft, ob alle Karten in der Hand die gleiche Farbe (Suit) haben.
    Wenn ja, gibt die Funktion True zurück, ansonsten False.
    """
    suits = [card.suit for card in hand]  # Extrahiert die Farben der Karten
    return len(set(suits)) == 1, max(hand, key=lambda card: rank_value(card.rank))   # Prüft, ob alle Farben gleich sind (Set hat nur ein Element)


# Prüft, ob die Hand eine Straße ist, also ob die Ränge aufeinanderfolgend sind
def is_straight(hand):
    """
    Überprüft, ob die Karten in der Hand aufeinanderfolgende Ränge haben.
    Behandelt auch den speziellen Fall von A-2-3-4-5 (Ace-low straight).
    """
    ranks = sorted([rank_value(card.rank) for card in hand])  # Sortiert die Ränge der Hand
    # Spezieller Fall: Ace kann als 1 verwendet werden in der Reihenfolge A-2-3-4-5 wobei 5 höchste Karte
    if ranks == [2, 3, 4, 5, 14]:
        return True, max(hand, key=lambda card: rank_value(card.rank) if rank_value(card.rank) != 14 else 5)
    # Überprüft, ob die Ränge eine lückenlose Folge bilden
    return all(ranks[i] + 1 == ranks[i + 1] for i in range(len(ranks) - 1)), max(hand, key=lambda card: rank_value(card.rank))


# Prüft, ob die Hand einen Vierling (four of a kind) enthält
def is_four_of_a_kind(hand):
    """
    Überprüft, ob die Hand vier Karten des gleichen Rangs enthält.
    Gibt True zurück, wenn dies der Fall ist, ansonsten False.
    """
    counts = get_rank_counts(hand)  # Zählt die Häufigkeiten der Ränge in der Hand
    if 4 in counts.values():
        four_of_a_kind_rank = max([card for card in hand if counts[card.rank] == 4],
                                  key=lambda card: rank_value(card.rank))
        kicker = max([card for card in hand if counts[card.rank] != 4], key=lambda card: rank_value(card.rank))
        return True, four_of_a_kind_rank, kicker
    return False, None, None

# Prüft, ob die Hand ein Full House enthält (drei Karten eines Rangs und zwei Karten eines anderen Rangs)
def is_full_house(hand):
    """
    Überprüft, ob die Hand ein Full House ist (drei gleiche Ränge und zwei gleiche Ränge).
    Gibt True zurück, wenn dies der Fall ist, ansonsten False.
    """
    counts = get_rank_counts(hand)  # Zählt die Häufigkeiten der Ränge in der Hand
    if 3 in counts.values() and 2 in counts.values():
        three_of_a_kind_rank = max([rank for rank, count in counts.items() if count == 3], key=rank_value)
        pair_rank = max([rank for rank, count in counts.items() if count == 2], key=rank_value)
        return True, three_of_a_kind_rank, pair_rank
    return False, None, None

# Prüft, ob die Hand einen Drilling (three of a kind) enthält
def is_three_of_a_kind(hand):
    """
    Überprüft, ob die Hand drei Karten des gleichen Rangs enthält.
    Gibt True zurück, wenn dies der Fall ist, ansonsten False.
    """
    counts = get_rank_counts(hand)  # Zählt die Häufigkeiten der Ränge in der Hand
    if 3 in counts.values():
        three_of_a_kind_rank = max([rank for rank, count in counts.items() if count == 3], key=rank_value)
        kickers = sorted([card for card in hand if card.rank != three_of_a_kind_rank],
                         key=lambda card: rank_value(card.rank), reverse=True)[:2]
        return True, three_of_a_kind_rank, kickers
    return False, None, None

# Prüft, ob die Hand zwei Paare enthält
def is_two_pair(hand):
    """
    Überprüft, ob die Hand zwei Paare enthält.
    Gibt True zurück, wenn dies der Fall ist, ansonsten False.
    """
    counts = get_rank_counts(hand)  # Zählt die Häufigkeiten der Ränge in der Hand
    if list(counts.values()).count(2) == 2:
        pairs = sorted([rank for rank, count in counts.items() if count == 2], key=rank_value, reverse=True)
        kicker = max([card for card in hand if card.rank not in pairs], key=lambda card: rank_value(card.rank))
        return True, pairs[0], pairs[1], kicker
    return False, None, None, None

# Prüft, ob die Hand ein Paar enthält
def is_one_pair(hand):
    """
    Überprüft, ob die Hand genau ein Paar enthält.
    Gibt True zurück, wenn dies der Fall ist, ansonsten False.
    """
    counts = get_rank_counts(hand)  # Zählt die Häufigkeiten der Ränge in der Hand
    if list(counts.values()).count(2) == 1:
        pair_rank = max([rank for rank, count in counts.items() if count == 2], key=rank_value)
        kickers = sorted([card for card in hand if card.rank != pair_rank], key=lambda card: rank_value(card.rank),
                         reverse=True)[:3]
        return True, pair_rank, kickers
    return False, None, None

# Gibt die Karte mit dem höchsten Rang in der Hand zurück
def high_card(hand):
    """
    Gibt die Karte mit dem höchsten Rang in der Hand zurück.
    Wird oft verwendet, wenn keine speziellen Kombinationen vorliegen.
    """
    return max(hand, key=lambda card: rank_value(card.rank))  # Bestimmt die Karte mit dem höchsten Rang
