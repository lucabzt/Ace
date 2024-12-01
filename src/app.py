from flask import Flask, jsonify

app = Flask(__name__)

# Example data (replace with real logic/data)
players_data = [
    {"id": 1, "name": "Player 1", "chips": 1000},
    {"id": 2, "name": "Player 2", "chips": 1000},
    {"id": 3, "name": "Player 3", "chips": 1000},
    {"id": 4, "name": "Player 4", "chips": 1000},
    {"id": 5, "name": "Player 5", "chips": 1000},
]

community_cards_data = [
    {"rank": "5", "suit": "hearts", "faceUp": True},
    {"rank": "7", "suit": "diamonds", "faceUp": True},
    {"rank": "Q", "suit": "spades", "faceUp": True},
    {"rank": "K", "suit": "clubs", "faceUp": True},
    {"rank": "A", "suit": "hearts", "faceUp": True},
]

dealer_index = 2  # Player 3 is the dealer (0-indexed)
pot = 500  # Example pot amount

# API Endpoints
@app.route('/api/players', methods=['GET'])
def get_players():
    return jsonify(players_data)

@app.route('/api/community-cards', methods=['GET'])
def get_community_cards():
    return jsonify(community_cards_data)

@app.route('/api/dealer', methods=['GET'])
def get_dealer():
    return jsonify({"dealerIndex": dealer_index})

@app.route('/api/pot', methods=['GET'])
def get_pot():
    return jsonify({"pot": pot})

if __name__ == '__main__':
    app.run(debug=True)
