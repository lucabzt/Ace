import logging
import os
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import random
from src.game.game_round import GameRound  # Import your game logic
from src.game.resources.player import Player

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Initialize the game state
player_names = ['Mr. Vorderbrügge', 'Mr. Huber', 'Mr. Bozzetti', 'Mr. Meierlohr', 'Dr. Oetker', 'Mr. Kemper',
                'Ms. Gantert', 'OG KEMPER']
players = [Player(name) for name in player_names]
game = GameRound(players, small_blind=10, big_blind=20)


# Start the game loop in a separate thread
def game_loop():
    while True:
        time.sleep(5)  # Delay for the game state update loop
        game.play_round()


threading.Thread(target=game_loop, daemon=True).start()


# Endpoints
@app.route('/players', methods=['GET'])
def get_players():
    """Get current state of players."""
    player_data = [
        {
            "name": player.name,
            "balance": player.balance,
            "bet": game.bets.get(player.name),
            "cards": [{"rank": card.rank.value, "suit": card.suit.value, "faceUp": True} for card in player.cards],
            "winProb": f"{player.win_prob:.2f}%",
            "folded": player in game.folded_players,
        }
        for player in players
    ]
    return jsonify(player_data)


@app.route('/community-cards', methods=['GET'])
def get_community_cards():
    """Get current community cards."""
    community_cards = [
        {"rank": card.rank.value, "suit": card.suit.value, "faceUp": True}
        for card in game.community_cards
    ]
    return jsonify(community_cards)


@app.route('/dealer', methods=['GET'])
def get_dealer():
    """Get the current dealer's index."""
    return jsonify({"dealerIndex": game.dealer_index})


@app.route('/pot', methods=['GET'])
def get_pot():
    """Get the current pot value."""
    return jsonify({"pot": game.pot})


# New Endpoints
@app.route('/place-bet', methods=['POST'])
def place_bet():
    """Allow a player to place a bet."""
    data = request.json
    player_name = data.get("playerName")
    amount = data.get("amount")

    player = next((p for p in players if p.name == player_name), None)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    try:
        game.current_bet = max(game.current_bet, amount)  # Update current bet
        player.balance -= amount
        game.pot += amount
        game.bets[player.name] += amount
        return jsonify({"message": f"{player.name} placed a bet of {amount}", "pot": game.pot})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/fold', methods=['POST'])
def fold():
    """Mark a player as folded."""
    data = request.json
    player_name = data.get("playerName")

    player = next((p for p in players if p.name == player_name), None)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    game.folded_players.add(player)
    return jsonify({"message": f"{player.name} has folded."})


@app.route('/next-round', methods=['POST'])
def next_round():
    """Proceed to the next round."""
    try:
        game.play_round()
        return jsonify({"message": "Next round started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reset-game', methods=['POST'])
def reset_game():
    """Reset the game to the initial state."""
    game.reset_game()
    return jsonify({"message": "Game has been reset"})


@app.route('/get-game-state', methods=['GET'])
def get_game_state():
    """Get the full game state."""
    state = {
        "players": [
            {
                "name": player.name,
                "balance": player.balance,
                "folded": player in game.folded_players,
                "cards": [{"rank": card.rank.value, "suit": card.suit.value} for card in player.cards],
                "winProb": f"{player.win_prob:.2f}%"
            }
            for player in players
        ],
        "communityCards": [
            {"rank": card.rank.value, "suit": card.suit.value} for card in game.community_cards
        ],
        "pot": game.pot,
        "dealerIndex": game.dealer_index,
        "currentBet": game.current_bet,
    }
    return jsonify(state)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
