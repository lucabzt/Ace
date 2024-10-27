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
    suits = [card.suit for card in hand]  # Extract the suits of each card
    is_flush_hand = len(set(suits)) == 1  # Check if all suits are the same

    if is_flush_hand:
        # Sort the hand by rank in descending order to identify the high card and kickers
        sorted_hand = sorted(hand, key=lambda card: rank_value(card.rank), reverse=True)

        # Assign the highest card and the next four kickers
        high_card = sorted_hand[0]
        kicker_1 = sorted_hand[1] if len(sorted_hand) > 1 else None
        kicker_2 = sorted_hand[2] if len(sorted_hand) > 2 else None
        kicker_3 = sorted_hand[3] if len(sorted_hand) > 3 else None
        kicker_4 = sorted_hand[4] if len(sorted_hand) > 4 else None

        return True, high_card, kicker_1, kicker_2, kicker_3, kicker_4

    return False, None, None, None, None, None

# Prüft, ob die Hand eine Straße ist, also ob die Ränge aufeinanderfolgend sind
def is_straight(hand):
    """
    Überprüft, ob die Karten in der Hand aufeinanderfolgende Ränge haben.
    Behandelt auch den speziellen Fall von A-2-3-4-5 (Ace-low straight).
    """
    ranks = sorted([rank_value(card.rank) for card in hand])  # Sortiert die Ränge der Hand
    # Spezieller Fall: Ace kann als 1 verwendet werden in der Reihenfolge A-2-3-4-5 wobei 5 höchste Karte
    if ranks == [2, 3, 4, 5, 14]:
        return True, next((card for card in hand if rank_value(card.rank) == 5), None)
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
    Checks if the hand contains three cards of the same rank.
    Returns True if that's the case, otherwise False.
    """
    counts = get_rank_counts(hand)  # Counts the frequencies of ranks in the hand

    if 3 in counts.values():
        # Identify the rank of the three-of-a-kind
        three_of_a_kind_rank = max([rank for rank, count in counts.items() if count == 3], key=rank_value)

        kicker_ranks = []

        # Use a for loop to add the ranks of the kickers
        for card in hand:
            if card.rank != three_of_a_kind_rank:
                kicker_ranks.append(rank_value(card.rank))

        # Sort the kicker ranks in descending order and select the top 2 kickers
        kicker_ranks = sorted(kicker_ranks, reverse=True)[:2]

        # Assign kickers individually for return
        kicker_1_rank = kicker_ranks[0] if len(kicker_ranks) > 0 else None
        kicker_2_rank = kicker_ranks[1] if len(kicker_ranks) > 1 else None

        return True, three_of_a_kind_rank, kicker_1_rank, kicker_2_rank

    return False, None, None, None
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
    Checks if the hand contains exactly one pair.
    Returns True if that's the case, otherwise False.
    """
    counts = get_rank_counts(hand)  # Counts the frequencies of ranks in the hand

    if list(counts.values()).count(2) == 1:
        # Identify the rank of the pair
        pair_rank = max([rank for rank, count in counts.items() if count == 2], key=rank_value)

        # Initialize an empty list to store kicker ranks
        kicker_ranks = []

        # Use a for loop to collect the ranks of the kickers
        for card in hand:
            if card.rank != pair_rank:
                kicker_ranks.append(rank_value(card.rank))

        # Sort the kicker ranks in descending order and select the top 3 kickers
        kicker_ranks = sorted(kicker_ranks, reverse=True)[:3]

        # Assign kickers individually for return
        kicker_1_rank = kicker_ranks[0] if len(kicker_ranks) > 0 else None
        kicker_2_rank = kicker_ranks[1] if len(kicker_ranks) > 1 else None
        kicker_3_rank = kicker_ranks[2] if len(kicker_ranks) > 2 else None

        return True, pair_rank, kicker_1_rank, kicker_2_rank, kicker_3_rank

    return False, None, None, None, None

# Gibt die Karte mit dem höchsten Rang in der Hand zurück
def high_card(hand):
    """
    Returns the highest card in the hand along with the next four highest kickers.
    Typically used when no other combinations are present.
    """
    # Sort the hand by rank in descending order
    sorted_hand = sorted(hand, key=lambda card: rank_value(card.rank), reverse=True)

    # Assign high card and four kickers individually
    high_card = sorted_hand[0]
    kicker_1 = sorted_hand[1] if len(sorted_hand) > 1 else None
    kicker_2 = sorted_hand[2] if len(sorted_hand) > 2 else None
    kicker_3 = sorted_hand[3] if len(sorted_hand) > 3 else None
    kicker_4 = sorted_hand[4] if len(sorted_hand) > 4 else None

    return high_card, kicker_1, kicker_2, kicker_3, kicker_4