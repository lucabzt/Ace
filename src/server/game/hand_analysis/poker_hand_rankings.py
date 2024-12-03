from collections import Counter

from src.game.resources.card import Rank


# Helper function to determine the number of different ranks in a hand
def get_rank_counts(hand):
    """
    Returns a Counter object representing the frequency of ranks in the hand.
    The hand is a list of Card objects.
    """
    ranks = [card.rank for card in hand]  # Extracts ranks from the hand
    return Counter(ranks)  # Counts occurrences of each rank


# Helper function to determine the value of a rank
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
    Returns the numeric value of a rank to compare card values.
    Example: TWO = 2, THREE = 3, ..., ACE = 14.
    """
    return rank_values[rank]  # Returns the corresponding value of a rank


# Checks if all cards in the hand have the same suit
def is_flush(hand):
    """
    Checks if all cards in the hand have the same suit.
    Returns True if so, otherwise False.
    """
    suits = [card.suit for card in hand]  # Extracts the suits of each card
    is_flush_hand = len(set(suits)) == 1  # Checks if all suits are the same

    if is_flush_hand:
        # Sort the hand by rank in descending order to identify the high card and kickers
        high, kicker_1, kicker_2, kicker_3, kicker_4 = high_card(hand)

        return True, high, kicker_1, kicker_2, kicker_3, kicker_4

    return False, None, None, None, None, None


# Checks if the hand is a straight, meaning ranks are consecutive
def is_straight(hand):
    """
    Checks if the cards in the hand have consecutive ranks.
    Also handles the special case of A-2-3-4-5 (Ace-low straight).
    """
    ranks = sorted([rank_value(card.rank) for card in hand])  # Sorts the ranks of the hand
    # Special case: Ace can be used as 1 in the sequence A-2-3-4-5 with 5 as the high card
    if ranks == [2, 3, 4, 5, 14]:
        return True, next((card for card in hand if rank_value(card.rank) == 5), None)
    # Checks if the ranks form a consecutive sequence
    return all(ranks[i] + 1 == ranks[i + 1] for i in range(len(ranks) - 1)), max(hand,
                                                                                 key=lambda card: rank_value(card.rank))


# Checks if the hand contains four cards of the same rank (Four of a Kind)
def is_four_of_a_kind(hand):
    """
    Checks if the hand contains four cards of the same rank.
    Returns True if that's the case, otherwise False.
    """
    counts = get_rank_counts(hand)  # Counts the frequencies of ranks in the hand
    if 4 in counts.values():
        four_of_a_kind_rank = max([card for card in hand if counts[card.rank] == 4],
                                  key=lambda card: rank_value(card.rank))
        kicker = max([card for card in hand if counts[card.rank] != 4], key=lambda card: rank_value(card.rank))
        return True, four_of_a_kind_rank, kicker
    return False, None, None


# Checks if the hand contains a Full House (three of one rank and two of another)
def is_full_house(hand):
    """
    Checks if the hand is a Full House (three of a kind and a pair).
    Returns True if that's the case, otherwise False.
    """
    counts = get_rank_counts(hand)  # Counts the frequencies of ranks in the hand
    if 3 in counts.values() and 2 in counts.values():
        three_of_a_kind_rank = max([rank for rank, count in counts.items() if count == 3], key=rank_value)
        pair_rank = max([rank for rank, count in counts.items() if count == 2], key=rank_value)
        return True, three_of_a_kind_rank, pair_rank
    return False, None, None


# Checks if the hand contains three cards of the same rank (Three of a Kind)
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


# Checks if the hand contains two pairs
def is_two_pair(hand):
    """
    Checks if the hand contains two pairs.
    Returns True if that's the case, otherwise False.
    """
    counts = get_rank_counts(hand)  # Counts the frequencies of ranks in the hand
    if list(counts.values()).count(2) == 2:
        pairs = sorted([rank for rank, count in counts.items() if count == 2], key=rank_value, reverse=True)
        kicker = max([card for card in hand if card.rank not in pairs], key=lambda card: rank_value(card.rank))
        return True, pairs[0], pairs[1], kicker
    return False, None, None, None


# Checks if the hand contains one pair
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


# Returns the highest card in the hand
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
