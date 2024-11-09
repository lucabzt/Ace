from enum import Enum


# Enum for the card suits
class Suit(Enum):
    HEARTS = 'HEARTS'
    DIAMONDS = 'DIAMONDS'
    SPADES = 'SPADES'
    CLUBS = 'CLUBS'


# Enum for the card ranks
class Rank(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'JACK'
    QUEEN = 'QUEEN'
    KING = 'KING'
    ACE = 'ACE'


suit_mapping = {
    Suit.HEARTS: "h",
    Suit.DIAMONDS: "d",
    Suit.SPADES: "s",
    Suit.CLUBS: "c",
}


rank_mapping = {
    Rank.TWO: "2",
    Rank.THREE: "3",
    Rank.FOUR: "4",
    Rank.FIVE: "5",
    Rank.SIX: "6",
    Rank.SEVEN: "7",
    Rank.EIGHT: "8",
    Rank.NINE: "9",
    Rank.TEN: "T",
    Rank.JACK: "J",
    Rank.QUEEN: "Q",
    Rank.KING: "K",
    Rank.ACE: "A",
}


# The Card class, using Suit and Rank enums
class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.abbreviation = rank_mapping[rank] + suit_mapping[suit]

    def __repr__(self):
        # Returns a user-friendly representation of the card
        return f"{self.rank.value} of {self.suit.value}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __lt__(self, other):
        """Less than method for comparing cards, only by rank."""
        if isinstance(other, Card):
            # Custom ordering for ranks
            rank_order = {
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
            return rank_order[self.rank] < rank_order[other.rank]
        return NotImplemented
