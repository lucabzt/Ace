# import required module
import threading
import time

from playsound3 import playsound
import os
import random

import src.game.hand_analysis.main


def play_winner_sound(winner):
    play_winners_sound([winner])


# Helper function to play a random sound file from a list
def play_random_sound(file_path):
    # Example: playing a random sound from four files
    # Generate the list of letters up to the specified count
    try:
        folder_path = os.path.join("../../assets/sounds/", file_path)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if files:
            # Select a random file from the list
            random_file = random.choice(files)
            # Play the selected file
            playsound(os.path.join(folder_path, random_file))
        else:
            print("No files found in the folder.")
    except Exception as e:
        print(e)


def play_all_sounds(file_path) -> threading.Thread:
    def play_sound():
        try:
            folder_path = os.path.join("../../assets/sounds/", file_path)
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            for file in files:
                playsound(os.path.join(folder_path, file))
        except Exception as e:
            print(e)

    # Create a thread to play sound in the background
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.start()
    return sound_thread


# Function to construct the sound paths for a card rank
def get_card_sound_paths(rank):
    rank_path = f"../../assets/sounds/Poker Cards/Card/Plural/{rank.upper()}"
    return [os.path.join(rank_path, f"{rank.upper()}{i}.mp3") for i in range(1, 5)]


# Function to construct paths for specific phrases
def get_announcement_path(phrase):
    base_path = "../../assets/sounds"
    paths = {
        "wins": [os.path.join(base_path, "Player Actions", "wins.mp3")],
        "full of": [os.path.join(base_path, "Winning Hands", "full of.mp3")],
        "and": [os.path.join(base_path, "Phrases", "and.mp3")]
    }
    return paths.get(phrase, [])


# Play player name sound
def play_player_name(name):
    play_random_sound(f"Players/{name}")


# Play the sound for a winning hand type
def play_hand_type(hand_type):


# Function to handle Full House announcement
def play_full_house(attributes):


# Function to handle a generic hand with attributes
def play_generic_hand(hand_type, attributes):



# Main function that plays the winner's sound based on hand type
def play_winners_sound(winners):
    for winner in winners:
        name, hand_type, (hand_cards, attributes) = winner

        # Switch-like structure for each hand type
        if hand_type == "Royal Flush":
            play_hand_type("Royal Flush") #No attr needed
        elif hand_type == "Straight Flush":
            play_generic_hand("Straight Flush", [attributes[0]]) #Attr = High of straight
        elif hand_type == "Four of a Kind":
            play_generic_hand("Four of a Kind", attributes[0]) #Attr = rank of quads
        elif hand_type == "Full House":
            play_full_house(attributes) #Attr = Trip Card rank, Pair Card rank
        elif hand_type == "Flush":
            play_generic_hand("Flush", attributes[0]) #Attr = High of Flush
        elif hand_type == "Straight":
            play_generic_hand("Straight", [attributes[0]]) #Attr = High of straigh
        elif hand_type == "Three of a Kind":
            play_generic_hand("Three of a Kind", attributes[0]) #Attr = Trip Card rank
        elif hand_type == "Two Pair":
            play_generic_hand("Two Pair", attributes[:2]) #Attr = High Pair, Low Pair rank
        elif hand_type == "One Pair":
            play_generic_hand("One Pair", attributes[0]) #Attr = Pair Card
        elif hand_type == "High Card":
            play_generic_hand("High Card", attributes[0]) #High Card

        # winning person
        play_player_name(name)
        play_random_sound("Player Actions/Win")

if __name__ == '__main__':
    play_winners_sound(src.game.hand_analysis.main.main())

