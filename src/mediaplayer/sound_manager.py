# import required module
from playsound3 import playsound

# array of winner
def play_winners_sound(winners):
    # for playing note.wav file
    playsound('../../assets/sounds/Poker Cards/Poker Cards/Card/Plural/FIVES.mp3')
    playsound('../../assets/sounds/Winning Hands/Winning Hands/full of.mp3')


# /*winner: (Name, Hand, ([Handkarten, Länge 5, sortiert - low to high], [attribut der hand]))*/
def play_winner_sound(winner):
    play_winners_sound([winner])

if __name__ == '__main__':
    play_winner_sound([])