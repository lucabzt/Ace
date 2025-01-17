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
from waitress import serve

import lyricsgenius
from server.src.game.utils.game_utils import display_spade_art
from server.src.game.game_round import GameRound  # Import your game logic
from server.src.game.resources.player import Player
from server.src.game.shared import SharedResources


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

# Your Genius API Access Token
genius = lyricsgenius.Genius("UUODLxcCpDdlIm_k8hqQvP-qYcQrfnvOB9ULnwDAS7LsQ-ZVtQwwJ7n-vUW-s2M3")

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


# Endpoints for Lyrics
@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    """Get the lyrics of a song based on input artist and song title."""
    artist = request.args.get('artist')
    song_title = request.args.get('title')

    if not artist or not song_title:
        return jsonify({"error": "Please provide both 'artist' and 'title' parameters."}), 400

    try:
        # Suche nach dem Song
        song = genius.search_song(song_title, artist)
        if song:
            # Rückgabe der Songtexte
            lyrics = song.lyrics
            return jsonify({"artist": artist, "title": song_title, "lyrics": lyrics})
        else:
            return jsonify({"error": "Lyrics not found."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Endpoints for Poker
@app.route('/players', methods=['GET'])
def get_players():
    """Get current state of players."""
    player_data = [
        {
            "name": player.name,
            "balance": player.balance,
            "pnl": game.pnl_matrix.get(player.name, []),
            "bet": game.bets.get(player.name),
            "cards": [{"rank": card.rank.value, "suit": card.suit.value, "faceUp": True} for card in player.cards],
            "probWin": round(player.win_prob, 2),
            "folded": player in game.folded_players,
            "actionPending": player.action_pending
        }
        for player in game.players
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
    return redirect(
        f"https://127.0.0.1:3000/spotify/#access_token={access_token}&refresh_token={refresh_token}&expires_at={expiration_timestamp}")


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


@app.route('/heatmap', methods=['GET'])
def heatmap():
    """Returns heatmap data for visualization."""
    heatmap_data = [
            {
                "x": "A",
                "y": "A",
                "heat": 0.85,
                "symbol": "\n 0"
            },
            {
                "x": "A",
                "y": "K",
                "heat": 0.65,
                "symbol": "o \n 5"
            },
            {
                "x": "A",
                "y": "Q",
                "heat": 0.64,
                "symbol": "o \n 8"
            },
            {
                "x": "A",
                "y": "J",
                "heat": 0.64,
                "symbol": "o \n 12"
            },
            {
                "x": "A",
                "y": "T",
                "heat": 0.63,
                "symbol": "o \n 18"
            },
            {
                "x": "A",
                "y": "9",
                "heat": 0.61,
                "symbol": "o \n 32"
            },
            {
                "x": "A",
                "y": "8",
                "heat": 0.6,
                "symbol": "o \n 39"
            },
            {
                "x": "A",
                "y": "7",
                "heat": 0.59,
                "symbol": "o \n 45"
            },
            {
                "x": "A",
                "y": "6",
                "heat": 0.58,
                "symbol": "o \n 51"
            },
            {
                "x": "A",
                "y": "5",
                "heat": 0.58,
                "symbol": "o \n 44"
            },
            {
                "x": "A",
                "y": "4",
                "heat": 0.57,
                "symbol": "o \n 46"
            },
            {
                "x": "A",
                "y": "3",
                "heat": 0.56,
                "symbol": "o \n 49"
            },
            {
                "x": "A",
                "y": "2",
                "heat": 0.55,
                "symbol": "o \n 54"
            },
            {
                "x": "K",
                "y": "A",
                "heat": 0.76,
                "symbol": "s \n 2"
            },
            {
                "x": "K",
                "y": "K",
                "heat": 0.82,
                "symbol": ""
            },
            {
                "x": "K",
                "y": "Q",
                "heat": 0.61,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "J",
                "heat": 0.61,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "T",
                "heat": 0.59,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "9",
                "heat": 0.58,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "8",
                "heat": 0.56,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "7",
                "heat": 0.55,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "6",
                "heat": 0.54,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "5",
                "heat": 0.53,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "4",
                "heat": 0.52,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "3",
                "heat": 0.51,
                "symbol": "u"
            },
            {
                "x": "K",
                "y": "2",
                "heat": 0.51,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "A",
                "heat": 0.66,
                "symbol": "s"
            },
            {
                "x": "Q",
                "y": "K",
                "heat": 0.63,
                "symbol": "s"
            },
            {
                "x": "Q",
                "y": "Q",
                "heat": 0.8,
                "symbol": ""
            },
            {
                "x": "Q",
                "y": "J",
                "heat": 0.58,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "T",
                "heat": 0.57,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "9",
                "heat": 0.55,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "8",
                "heat": 0.54,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "7",
                "heat": 0.52,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "6",
                "heat": 0.51,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "5",
                "heat": 0.5,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "4",
                "heat": 0.49,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "3",
                "heat": 0.48,
                "symbol": "u"
            },
            {
                "x": "Q",
                "y": "2",
                "heat": 0.47,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "A",
                "heat": 0.65,
                "symbol": "s"
            },
            {
                "x": "J",
                "y": "K",
                "heat": 0.63,
                "symbol": "s"
            },
            {
                "x": "J",
                "y": "Q",
                "heat": 0.6,
                "symbol": "s"
            },
            {
                "x": "J",
                "y": "J",
                "heat": 0.77,
                "symbol": ""
            },
            {
                "x": "J",
                "y": "T",
                "heat": 0.55,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "9",
                "heat": 0.53,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "8",
                "heat": 0.51,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "7",
                "heat": 0.5,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "6",
                "heat": 0.48,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "5",
                "heat": 0.47,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "4",
                "heat": 0.46,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "3",
                "heat": 0.45,
                "symbol": "u"
            },
            {
                "x": "J",
                "y": "2",
                "heat": 0.44,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "A",
                "heat": 0.65,
                "symbol": "s"
            },
            {
                "x": "T",
                "y": "K",
                "heat": 0.62,
                "symbol": "s"
            },
            {
                "x": "T",
                "y": "Q",
                "heat": 0.59,
                "symbol": "s"
            },
            {
                "x": "T",
                "y": "J",
                "heat": 0.58,
                "symbol": "s"
            },
            {
                "x": "T",
                "y": "T",
                "heat": 0.75,
                "symbol": ""
            },
            {
                "x": "T",
                "y": "9",
                "heat": 0.52,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "8",
                "heat": 0.5,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "7",
                "heat": 0.48,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "6",
                "heat": 0.46,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "5",
                "heat": 0.44,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "4",
                "heat": 0.44,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "3",
                "heat": 0.43,
                "symbol": "u"
            },
            {
                "x": "T",
                "y": "2",
                "heat": 0.42,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "A",
                "heat": 0.63,
                "symbol": "s"
            },
            {
                "x": "9",
                "y": "K",
                "heat": 0.6,
                "symbol": "s"
            },
            {
                "x": "9",
                "y": "Q",
                "heat": 0.58,
                "symbol": "s"
            },
            {
                "x": "9",
                "y": "J",
                "heat": 0.56,
                "symbol": "s"
            },
            {
                "x": "9",
                "y": "T",
                "heat": 0.54,
                "symbol": "s"
            },
            {
                "x": "9",
                "y": "9",
                "heat": 0.72,
                "symbol": ""
            },
            {
                "x": "9",
                "y": "8",
                "heat": 0.48,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "7",
                "heat": 0.46,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "6",
                "heat": 0.44,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "5",
                "heat": 0.43,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "4",
                "heat": 0.41,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "3",
                "heat": 0.4,
                "symbol": "u"
            },
            {
                "x": "9",
                "y": "2",
                "heat": 0.39,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "A",
                "heat": 0.62,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "K",
                "heat": 0.58,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "Q",
                "heat": 0.56,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "J",
                "heat": 0.54,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "T",
                "heat": 0.52,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "9",
                "heat": 0.51,
                "symbol": "s"
            },
            {
                "x": "8",
                "y": "8",
                "heat": 0.69,
                "symbol": ""
            },
            {
                "x": "8",
                "y": "7",
                "heat": 0.45,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "6",
                "heat": 0.43,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "5",
                "heat": 0.41,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "4",
                "heat": 0.39,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "3",
                "heat": 0.37,
                "symbol": "u"
            },
            {
                "x": "8",
                "y": "2",
                "heat": 0.37,
                "symbol": "u"
            },
            {
                "x": "7",
                "y": "A",
                "heat": 0.61,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "K",
                "heat": 0.58,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "Q",
                "heat": 0.54,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "J",
                "heat": 0.52,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "T",
                "heat": 0.51,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "9",
                "heat": 0.49,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "8",
                "heat": 0.48,
                "symbol": "s"
            },
            {
                "x": "7",
                "y": "7",
                "heat": 0.66,
                "symbol": ""
            },
            {
                "x": "7",
                "y": "6",
                "heat": 0.42,
                "symbol": "u"
            },
            {
                "x": "7",
                "y": "5",
                "heat": 0.41,
                "symbol": "u"
            },
            {
                "x": "7",
                "y": "4",
                "heat": 0.39,
                "symbol": "u"
            },
            {
                "x": "7",
                "y": "3",
                "heat": 0.37,
                "symbol": "u"
            },
            {
                "x": "7",
                "y": "2",
                "heat": 0.35,
                "symbol": "u"
            },
            {
                "x": "6",
                "y": "A",
                "heat": 0.6,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "K",
                "heat": 0.57,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "Q",
                "heat": 0.54,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "J",
                "heat": 0.51,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "T",
                "heat": 0.49,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "9",
                "heat": 0.47,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "8",
                "heat": 0.46,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "7",
                "heat": 0.45,
                "symbol": "s"
            },
            {
                "x": "6",
                "y": "6",
                "heat": 0.63,
                "symbol": ""
            },
            {
                "x": "6",
                "y": "5",
                "heat": 0.4,
                "symbol": "u"
            },
            {
                "x": "6",
                "y": "4",
                "heat": 0.38,
                "symbol": "u"
            },
            {
                "x": "6",
                "y": "3",
                "heat": 0.36,
                "symbol": "u"
            },
            {
                "x": "6",
                "y": "2",
                "heat": 0.34,
                "symbol": "u"
            },
            {
                "x": "5",
                "y": "A",
                "heat": 0.6,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "K",
                "heat": 0.56,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "Q",
                "heat": 0.53,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "J",
                "heat": 0.5,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "T",
                "heat": 0.47,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "9",
                "heat": 0.46,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "8",
                "heat": 0.45,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "7",
                "heat": 0.44,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "6",
                "heat": 0.43,
                "symbol": "s"
            },
            {
                "x": "5",
                "y": "5",
                "heat": 0.6,
                "symbol": ""
            },
            {
                "x": "5",
                "y": "4",
                "heat": 0.38,
                "symbol": "u"
            },
            {
                "x": "5",
                "y": "3",
                "heat": 0.36,
                "symbol": "u"
            },
            {
                "x": "5",
                "y": "2",
                "heat": 0.34,
                "symbol": "u"
            },
            {
                "x": "4",
                "y": "A",
                "heat": 0.59,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "K",
                "heat": 0.55,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "Q",
                "heat": 0.52,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "J",
                "heat": 0.49,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "T",
                "heat": 0.47,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "9",
                "heat": 0.44,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "8",
                "heat": 0.43,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "7",
                "heat": 0.42,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "6",
                "heat": 0.41,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "5",
                "heat": 0.41,
                "symbol": "s"
            },
            {
                "x": "4",
                "y": "4",
                "heat": 0.57,
                "symbol": ""
            },
            {
                "x": "4",
                "y": "3",
                "heat": 0.35,
                "symbol": "u"
            },
            {
                "x": "4",
                "y": "2",
                "heat": 0.33,
                "symbol": "u"
            },
            {
                "x": "3",
                "y": "A",
                "heat": 0.58,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "K",
                "heat": 0.54,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "Q",
                "heat": 0.51,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "J",
                "heat": 0.48,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "T",
                "heat": 0.46,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "9",
                "heat": 0.43,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "8",
                "heat": 0.41,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "7",
                "heat": 0.4,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "6",
                "heat": 0.4,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "5",
                "heat": 0.4,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "4",
                "heat": 0.39,
                "symbol": "s"
            },
            {
                "x": "3",
                "y": "3",
                "heat": 0.54,
                "symbol": ""
            },
            {
                "x": "3",
                "y": "2",
                "heat": 0.32,
                "symbol": "u"
            },
            {
                "x": "2",
                "y": "A",
                "heat": 0.57,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "K",
                "heat": 0.53,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "Q",
                "heat": 0.5,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "J",
                "heat": 0.47,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "T",
                "heat": 0.45,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "9",
                "heat": 0.42,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "8",
                "heat": 0.4,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "7",
                "heat": 0.38,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "6",
                "heat": 0.38,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "5",
                "heat": 0.38,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "4",
                "heat": 0.37,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "3",
                "heat": 0.36,
                "symbol": "s"
            },
            {
                "x": "2",
                "y": "2",
                "heat": 0.5,
                "symbol": ""
            }
    ]
    return jsonify(heatmap_data)


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


@app.route("/")
def home():
    return "Welcome to your Flask app running on Uvicorn!"


# Run the Flask app
if __name__ == '__main__':
    threading.Thread(target=game_loop, daemon=True).start()
    display_spade_art()  # Display spade art on game start

    DEBUG = True

    if DEBUG:
        app.run(debug=True, host='127.0.0.1', port=5000
                , ssl_context=('./cert.pem', './key.pem')
                )
    else:
        serve(app, host='0.0.0.0', port=5000)
