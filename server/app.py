import base64
import logging
import random
import string
import threading
import time
import urllib.parse

import requests
from flask import Flask, redirect, request, session
from flask import jsonify
from flask import render_template
from flask_cors import CORS

from src.game.utils.game_utils import display_spade_art
from src.game.game_round import GameRound  # Import your game logic
from src.game.resources.player import Player
from src.game.shared import SharedResources


def generate_random_string(length):
    """Generate a random string for the state parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


app = Flask(__name__)

app.secret_key = 'a_random_secret_key_12345'  # Required for session handling (optional)

CLIENT_ID = "258c86af6a9e45ac8fac5185cceff480"
CLIENT_SECRET = "e5c969b18de0458a95552515897cd7fc"

REDIRECT_URI = f"https://localhost:5000/callback"

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Enable CORS for all routes
CORS(app)

# Initialize the game state
player_names = ['Bozzetti', 'Huber', 'Rogg', 'Meierlohr', 'Hoerter', 'Simon',
                'Vorderbruegge', 'Maier']
players = [Player(name) for name in player_names]
shared_resources = SharedResources()
game = GameRound(players, small_blind=10, big_blind=20, shared_resources=shared_resources)


@app.route('/', methods=['GET'])
def get_home():
    return render_template("index.html")

@app.route('/index.html', methods=['GET'])
def get_index():
    return render_template("index.html")


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
            "probWin": round(player.win_prob, 2),
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

    # Add placeholder cards if there are less than 5 cards
    while len(community_cards) < 5:
        community_cards.append({"rank": None, "suit": None, "faceUp": False})

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

@app.route('/player-action', methods=['POST'])
def update_player_action():
    data = request.json
    action = data.get("action")

    if not action:
        return jsonify({"status": "error", "message": "Missing action."}), 400

    shared_resources.player_action_queue.put(action)
    print(f"Action added to queue: {action}")
    return jsonify({"status": "ok"}), 200



@app.route('/login')
def login():
    """Redirect the user to Spotify's authorization endpoint."""
    state = generate_random_string(16)  # Generate a random state string
    session['state'] = state  # Save state to session for validation later

    scope = "user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public "  # Permissions your app requests
    #scope = "user-read-private user-read-email streaming user-modify-playback-state"
        
    # Construct the Spotify authorization URL
    query_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "state": state
    }

    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(query_params)}"
    print("Redirect to authoreize...")
    return redirect(auth_url)  # Redirect to Spotify's login page


@app.route('/callback')
def callback():
    """Handle the Spotify authorization callback."""

    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Authorization failed"}), 400

    print("Got callback: " + code)

    # Exchange authorization code for an access token
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch access token"}), response.status_code
    


    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in")  # Time in seconds
    expiration_timestamp = int(time.time()) + expires_in

    #print("Got tokens: (status code)" + response.status_code + " -> token: " + access_token)

    # Redirect to React app with tokens
    return redirect(f"https://127.0.0.1:3000/spotify/#access_token={access_token}&refresh_token={refresh_token}&expires_at={expiration_timestamp}")


@app.route('/refresh_token', methods=['GET'])
def refresh_token():
    """Handle token refresh."""
    refresh_token = request.args.get('refresh_token')
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    response = requests.post(
        SPOTIFY_TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to refresh token"}), response.status_code

    return jsonify(response.json())


def game_loop():
    try:
        while True:
            time.sleep(5)  # Delay for the game state update loop
            game.play_round()
    except KeyboardInterrupt:
        print("Stopping Game...")
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            print('Not running with the Werkzeug Server')
        func()
        return 0


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Run the Flask app
if __name__ == '__main__':
    threading.Thread(target=game_loop, daemon=True, static_url_path='', static_folder='/static/client/').start()
    display_spade_art()  # Display spade art on game start
    app.run(debug=False, host='127.0.0.1', port=5000, ssl_context=('./server/cert.pem', './server/key.pem'))

