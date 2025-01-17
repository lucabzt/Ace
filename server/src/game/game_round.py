import csv
import time
from datetime import datetime

from server.src.engine import holdem_calc, parallel_holdem_calc
from server.src.game.betting_round import BettingRound
from server.src.game.hand_analysis.winner_determiner import WinnerAnalyzer
from server.src.game.input import modify_game_settings
from server.src.game.resources.player import Player
from server.src.game.resources.poker_deck import Deck
from server.src.game.utils.game_utils import display_spade_art, display_new_round


class GameRound:
    def __init__(self, players, small_blind, big_blind, shared_resources):
        if len(players) < 2:
            raise ValueError("Mindestens zwei Spieler sind erforderlich.")
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.current_bet = 0
        self.bets = {player.name: 0 for player in players}
        self.folded_players = set()
        self.active_players = self.players.copy()
        self.small_blind_index = 0
        self.dealer_index = 0
        self.big_blind_player = None
        self.small_blind_player = None
        self.round_logs = []  # Logs for each round
        self.exit_game = False  # Flag to indicate game exit
        self.shared_resources = shared_resources
        self.pnl_matrix = {player.name: [] for player in players}
        self.play_sound = True

        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        for player in self.players:
            # Every player starts with pnl of 0
            self.pnl_matrix[player.name].append([timestamp, 0])

    def play_round(self):
        """Plays a complete round of poker, with option to modify settings before starting."""
        if input("Would you like to make any changes before starting the round? (yes/no): ").lower() == 'yes':
            modify_game_settings(self)  # Use the input module's method
            if self.exit_game:
                self.save_logs()
                print("Game exited.")
                return  # Exit game if user chose to

        display_new_round()
        self.assign_blinds()
        self.deal_private_cards()
        betting_round = BettingRound(self.players, self.pot, self.current_bet, self.small_blind_index,
                                     self.folded_players, self.active_players, self.bets,
                                     self.update_display, self, self.shared_resources, self.play_sound)

        print("---------------")
        # Pre-Flop Betting
        if self.play_betting_round(betting_round, 'Pre-Flop', False):
            self.update_pnl_matrix()
            self.reset_game()
            return

        # Deal Flop
        self.deal_community_cards(3)
        print("---------------")

        # Flop Betting
        if self.play_betting_round(betting_round, 'Flop', False):
            self.update_pnl_matrix()
            self.reset_game()
            return

        # Turn
        self.deal_community_cards(1)
        print("---------------")

        # Turn Betting
        if self.play_betting_round(betting_round, 'Turn', False):
            self.update_pnl_matrix()
            self.reset_game()
            return

        # River
        self.deal_community_cards(1)

        # River Betting
        if self.play_betting_round(betting_round, 'River', True):
            self.update_pnl_matrix()
            self.reset_game()
            return

        # Showdown if more than one player remains
        self.showdown()

        # Update PNL matrix
        self.update_pnl_matrix()

        # Reset for next game
        self.reset_game()

    def play_betting_round(self, betting_round, current_round, river):
        self.calculate_probabilities(river)
        betting_round.execute(current_round)
        self.log_round(current_round)
        print("---------------")
        if self.declare_winner_if_only_one_remaining():
            return True
        return False

    def assign_blinds(self):
        """Assigns small and big blinds to players and handles the initial bets."""
        print("\n--- BLINDS ---")
        self.small_blind_player = self.players[self.small_blind_index]
        self.big_blind_player = self.players[(self.small_blind_index + 1) % len(self.players)]
        self.dealer_index = (self.small_blind_index - 1) % len(self.players)

        # Deduct blinds from player balances
        if self.small_blind_player.balance >= self.small_blind:
            self.small_blind_player.balance -= self.small_blind
            self.bets[self.small_blind_player.name] += self.small_blind
            self.pot += self.small_blind
        else:
            raise ValueError(f"{self.small_blind_player.name} does not have enough chips for the small blind.")

        if self.big_blind_player.balance >= self.big_blind:
            self.big_blind_player.balance -= self.big_blind
            self.bets[self.big_blind_player.name] += self.big_blind
            self.pot += self.big_blind
            self.current_bet = self.big_blind  # Set the minimum call amount
        else:
            raise ValueError(f"{self.big_blind_player.name} does not have enough chips for the big blind.")

        print(f"{self.small_blind_player.name} posts small blind: {self.small_blind}")
        print(f"{self.big_blind_player.name} posts big blind: {self.big_blind}")
        print(f"The dealer is {self.players[self.dealer_index].name}")

    def rotate_blinds(self):
        """Rotates blinds and dealer to the next players after each round."""
        self.small_blind_index = (self.small_blind_index + 1) % len(self.players)
        self.dealer_index = (self.dealer_index - 1) % len(self.players)  # Rotate dealer to the next player

    def deal_private_cards(self):
        """Deals two private cards to each player."""
        print("\n--- DEALING PRIVATE CARDS ---")
        for _ in range(2):
            for index, player in enumerate(self.players):
                card = self.deck.deal_card()
                player.receive_card(card)
                print(f"{player.name} erhält Karte: {card}")

    def deal_community_cards(self, number):
        """Deals the specified number of community cards."""
        print("\n--- DEALING COMMUNITY CARDS ---")
        for _ in range(number):
            card = self.deck.deal_card()
            self.community_cards.append(card)
            print(f"Gemeinschaftskarte: {card}")

    def showdown(self):
        """Determines the winner(s) and distributes the pot."""
        print("\n--- SHOWDOWN ---")

        if not self.active_players:
            print("Alle Spieler haben gefoldet. Pot bleibt unverteilt.")
            return

        community = self.community_cards
        player_hands = [(player, player.get_best_hand(community)) for player in self.active_players]

        analyzer = WinnerAnalyzer([(player.name, best_hand[1]) for player, best_hand in player_hands])
        winners = analyzer.analyze_winners()

        if len(winners) == 1:
            winner = winners[0]
            winning_player = next(player for player in self.players if player.name == winner[0])
            winning_player.add_balance(self.pot)
            print(f"Gewinner ist {winning_player.name} mit {winner[1]}. Pot: {self.pot}")
        else:
            winner_info = winners[0]
            split_amount = self.pot // len(winners)
            winner_names = ', '.join([winner[0] for winner in winners])
            print(
                f"Es gibt einen Split-Pot zwischen: {winner_names} mit {winner_info[1]}. Jeder erhält: {split_amount}")
            for winner in winners:
                winning_player = next(player for player in self.players if player.name == winner[0])
                winning_player.add_balance(split_amount)

    def declare_winner_if_only_one_remaining(self):
        """Checks if only one player remains and declares them the winner."""
        if len(self.active_players) == 1:
            winner = self.active_players[0]
            winner.add_balance(self.pot)
            print(f"{winner.name} gewinnt {self.pot}, da alle anderen Spieler gefoldet haben.")
            return True
        return False

    def reset_game(self):
        """Resets the game state for the next round and rotates blinds."""
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.bets = {player.name: 0 for player in self.players}
        self.folded_players = set()
        self.active_players = self.players.copy()

        for player in self.players:
            player.clear_cards()

        self.rotate_blinds()  # Move blinds and dealer to the next players

    def update_pnl_matrix(self):
        """Update PnL matrix for all players."""
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        for player in self.players:
            # Check if the player is already in the matrix, add if not
            if player.name not in self.pnl_matrix:
                self.pnl_matrix[player.name] = []  # Add player to the matrix

            # Calculate PnL as the difference between the current balance and the absolute investment
            pnl = player.balance - player.absolute_investment
            # Append the PnL value with the current timestamp
            self.pnl_matrix[player.name].append([timestamp, pnl])

        # Debug or log the updated PnL matrix
        # print("Updated pnl_matrix:", self.pnl_matrix)

    def calculate_probabilities(self, river=False):
        # Create abbreviations for community and player cards
        community_cards = [c.abbreviation for c in self.community_cards]
        player_cards = []

        # Add cards from each player to player cards
        for player in self.active_players:
            player_cards.extend([c.abbreviation for c in player.cards])

        # Use engine to calculate probs: SCHULDIG: DESHALB KACKE MIT TERMINAL OUTPUT
        # Can use parallel to be faster
        probs = parallel_holdem_calc.calculate(community_cards, False, 10e3, None, player_cards, False)

        print(probs)

        # probs = holdem_calc.calculate(community_cards, False, 10e3, None, player_cards, False)

        # Update probs in player objects
        for i in range(len(self.active_players)):
            self.active_players[i].win_prob = probs[i + 1] * 100
            # pass

    def log_round(self, round_name):
        """Logs the current state of the game after each betting round."""
        log_entry = {
            'round': round_name,
            'pot': self.pot,
            'community_cards': [str(card) for card in self.community_cards],
            'player_bets': {player.name: self.bets[player.name] for player in self.players},
            'player_balances': {player.name: player.balance for player in self.players}
        }
        self.round_logs.append(log_entry)

    def save_logs(self):
        """Saves the game log to a CSV file upon exit."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"poker_game_log_{timestamp}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['round', 'pot', 'community_cards', 'player_bets', 'player_balances']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.round_logs:
                writer.writerow({
                    'round': entry['round'],
                    'pot': entry['pot'],
                    'community_cards': ', '.join(entry['community_cards']),
                    'player_bets': ', '.join([f"{k}: {v}" for k, v in entry['player_bets'].items()]),
                    'player_balances': ', '.join([f"{k}: {v}" for k, v in entry['player_balances'].items()])
                })
        print(f"Game log saved as {filename}.")

    def update_display(self):
        pass

    def set_pot(self, val):
        self.pot = val


def main():
    # Initialisiere Spieler
    player_names = ['Alice', 'Bob', 'Charlie']
    players = [Player(name) for name in player_names]

    # Initialisiere das Spiel
    game = GameRound(players, small_blind=10, big_blind=20)

    # Simuliere eine Pokerrunde
    game.play_round()


if __name__ == "__main__":
    main()
