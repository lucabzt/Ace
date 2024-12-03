from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Example data
players_data = [
    {
        "name": "Mr. Vorderbrügge",
        "probWin": "30%",
        "balance": 150,
        "bet": 20,
        "folded": False,
        "cards": [
            {"rank": "queen", "suit": "spades", "faceUp": True},
            {"rank": "jack", "suit": "hearts", "faceUp": True},
        ],
    },
    {
        "name": "Mr. Huber",
        "probWin": "75%",
        "balance": 250,
        "bet": 100,
        "folded": True,
        "cards": [
            {"rank": "10", "suit": "diamonds", "faceUp": False},
            {"rank": "9", "suit": "clubs", "faceUp": False},
        ],
    },
    {
        "name": "Mr. Bozzetti",
        "probWin": "50%",
        "balance": 50,
        "bet": 50,
        "folded": False,
        "cards": [
            {"rank": "ace", "suit": "clubs", "faceUp": True},
            {"rank": "king", "suit": "diamonds", "faceUp": True},
        ],
    },
    {
        "name": "Mr. Meierlohr",
        "probWin": "60%",
        "balance": 120,
        "bet": 70,
        "folded": False,
        "cards": [
            {"rank": "8", "suit": "hearts", "faceUp": True},
            {"rank": "8", "suit": "spades", "faceUp": True},
        ],
    },
    {
        "name": "Dr. Oetker",
        "probWin": "85%",
        "balance": 300,
        "bet": 150,
        "folded": False,
        "cards": [
            {"rank": "2", "suit": "clubs", "faceUp": True},
            {"rank": "3", "suit": "clubs", "faceUp": True},
        ],
    },
    {
        "name": "Mr. Kemper",
        "probWin": "55%",
        "balance": 200,
        "bet": 50,
        "folded": False,
        "cards": [
            {"rank": "jack", "suit": "diamonds", "faceUp": True},
            {"rank": "10", "suit": "hearts", "faceUp": True},
        ],
    },
    {
        "name": "Ms. Gantert",
        "probWin": "55%",
        "balance": 200,
        "bet": 50,
        "folded": False,
        "cards": [
            {"rank": "jack", "suit": "diamonds", "faceUp": True},
            {"rank": "10", "suit": "hearts", "faceUp": True},
        ],
    },
    {
        "name": "OG KEMPER",
        "probWin": "55%",
        "balance": 200,
        "bet": 50,
        "folded": False,
        "cards": [
            {"rank": "jack", "suit": "diamonds", "faceUp": True},
            {"rank": "10", "suit": "hearts", "faceUp": True},
        ],
    },
]

# Initial community cards
community_cards_data = [
    {"rank": "5", "suit": "hearts", "faceUp": True},
    {"rank": "7", "suit": "diamonds", "faceUp": True},
    {"rank": "10", "suit": "spades", "faceUp": True},
    {"rank": "ACE", "suit": "clubs", "faceUp": True},
    {"rank": "JACK", "suit": "hearts", "faceUp": True},
]

dealer_index = 2  # Start with Player 3 as the dealer
pot = 700


# Helper function to generate a random card
def generate_random_card():
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
    suits = ["hearts", "diamonds", "clubs", "spades"]
    return {"rank": random.choice(ranks), "suit": random.choice(suits),
            "faceUp": random.choice([True, True, True, False])}


# Periodic updates
def periodic_update():
    global dealer_index, community_cards_data
    while True:
        time.sleep(1)  # Wait 1 second between updates

        # Rotate dealer
        dealer_index = (dealer_index + 1) % len(players_data)

        # Rotate community cards
        community_cards_data = community_cards_data[1:] + [community_cards_data[0]]

        # Randomly update player data
        for player in players_data:
            if random.random() < 0.5:  # 50% chance to update a player's data
                player["cards"] = [generate_random_card(), generate_random_card()]
                player["folded"] = random.choice([True, False, False, False])


# Start the periodic updates in a separate thread
threading.Thread(target=periodic_update, daemon=True).start()


@app.route('/players', methods=['GET'])
def get_players():
    return jsonify(players_data)


@app.route('/community-cards', methods=['GET'])
def get_community_cards():
    return jsonify(community_cards_data)


@app.route('/dealer', methods=['GET'])
def get_dealer():
    return jsonify({"dealerIndex": dealer_index})


@app.route('/pot', methods=['GET'])
def get_pot():
    return jsonify({"pot": pot})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
