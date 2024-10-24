from enum import Enum


# Enum for the card suits
class Suit(Enum):
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    SPADES = 'spades'
    CLUBS = 'clubs'


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
    JACK = 'jack'
    QUEEN = 'queen'
    KING = 'king'
    ACE = 'ace'


# The Card class, using Suit and Rank enums
class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        # Returns a user-friendly representation of the card
        return f"{self.rank.value} of {self.suit.value}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __hash__(self):
        return hash((self.rank, self.suit))