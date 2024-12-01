from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Example data
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
    {"rank": "10", "suit": "spades", "faceUp": True},
    {"rank": "8", "suit": "clubs", "faceUp": True},
    {"rank": "JACK", "suit": "hearts", "faceUp": True},
]

dealer_index = 2
pot = 500

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