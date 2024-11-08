from src.game.game_utils import display_spade_art, display_new_round
from src.game.hand_analysis.winner_determiner import WinnerAnalyzer
from src.game.input import get_player_action
from src.game.resources.player import Player
from src.game.resources.poker_deck import Deck


class GameRound:
    def __init__(self, players, small_blind, big_blind):
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
        self.small_blind_index = 0
        self.big_blind_player = None
        self.small_blind_player = None

    def modify_game_settings(self):
        """Allows the user to modify game settings before each round."""
        print("\n--- MODIFY GAME SETTINGS ---")
        print("Options: 1) Add player, 2) Remove player, 3) Give balance to player, 4) Change blind sizes, 5) Continue")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            player_name = input("Enter the new player's name: ")
            if player_name and player_name not in [player.name for player in self.players]:
                self.players.append(Player(player_name))
                self.bets[player_name] = 0
                print(f"Player {player_name} has been added.")
            else:
                print("Invalid or duplicate player name.")

        elif choice == '2':
            player_name = input("Enter the player's name to remove: ")
            self.players = [player for player in self.players if player.name != player_name]
            if player_name in self.bets:
                del self.bets[player_name]
            print(f"Player {player_name} has been removed.")

        elif choice == '3':
            player_name = input("Enter the player's name to give balance: ")
            player = next((p for p in self.players if p.name == player_name), None)
            if player:
                amount = int(input(f"Enter the amount to give to {player_name}: "))
                player.balance += amount
                print(f"{player_name} now has {player.balance} chips.")
            else:
                print("Player not found.")

        elif choice == '4':
            self.small_blind = int(input("Enter new small blind: "))
            self.big_blind = int(input("Enter new big blind: "))
            print(f"Blinds updated. Small Blind: {self.small_blind}, Big Blind: {self.big_blind}")

        elif choice == '5':
            print("Continuing without changes.")
        else:
            print("Invalid choice. No changes made.")

    def assign_blinds(self):
        """Assigns small and big blinds to players and handles the initial bets."""
        print("\n--- BLINDS ---")
        self.small_blind_player = self.players[self.small_blind_index]
        self.big_blind_player = self.players[(self.small_blind_index + 1) % len(self.players)]

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

    def rotate_blinds(self):
        """Rotates blinds to the next players after each round."""
        self.small_blind_index = (self.small_blind_index + 1) % len(self.players)

    def deal_private_cards(self):
        """Deals two private cards to each player."""
        print("\n--- DEALING PRIVATE CARDS ---")
        for _ in range(2):
            for player in self.players:
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

    def betting_round(self, round_name):
        """Executes a betting round with players matching, raising, or folding as needed."""
        print(f"\n--- {round_name.upper()} BETTING ---")

        active_players = [player for player in self.players if player.name not in self.folded_players]

        # Determine the starting player for the betting round
        if round_name == 'Pre-Flop':
            start_index = (self.small_blind_index + 2) % len(self.players)
        else:
            start_index = next((i for i, player in enumerate(self.players) if player.name not in self.folded_players),
                               0)

        player_order = active_players[start_index:] + active_players[:start_index]

        # Track which players have matched the current bet
        players_in_round = {player.name: False for player in active_players}
        last_raiser = None

        while not all(
players_in_round[player.name] for player in active_players if player.name not in self.folded_players):

            for player in player_order:
                if player.name in self.folded_players:
                    continue  # Skip folded players

                # Skip if this is the player who last raised and everyone else has called or folded
                if last_raiser == player.name and all(
                        players_in_round[p.name] for p in active_players if p.name not in self.folded_players):
                    return  # End betting round

                to_call = self.current_bet - self.bets[player.name]
                action = get_player_action(player, to_call)

                if action == 'fold':
                    self.folded_players.add(player.name)
                    print(f"{player.name} folds.")
                elif action == 'check':
                    call_amount = to_call
                    if call_amount == 0:
                        players_in_round[player.name] = True
                        print(f"{player.name} checks")
                    else:
                        raise ValueError(f"Can't check! {player.name} has to call: {call_amount}/raise/fold!")
                elif action == 'call':
                    call_amount = to_call
                    if player.balance >= call_amount:
                        player.balance -= call_amount
                        self.bets[player.name] += call_amount
                        self.pot += call_amount
                        players_in_round[player.name] = True
                        print(f"{player.name} calls: {call_amount}")
                    else:
                        raise ValueError(f"{player.name} does not have enough chips to call.")
                elif action.startswith('raise'):
                    _, raise_amount = action.split()
                    raise_amount = int(raise_amount)
                    total_bet = to_call + raise_amount

                    if player.balance >= total_bet:
                        player.balance -= total_bet
                        self.bets[player.name] += total_bet
                        self.pot += total_bet
                        self.current_bet += raise_amount  # Update the highest bet
                        print(f"{player.name} raises by {raise_amount}")

                        # Update last raiser and reset players_in_round for a new round of calling
                        last_raiser = player.name
                        players_in_round = {p.name: (p.name in self.folded_players) for p in active_players}
                        players_in_round[player.name] = True  # Player who raised has already matched their own bet
                    else:
                        raise ValueError(f"{player.name} does not have enough chips to raise.")

                # Break if only one active player remains
                if len([p for p in active_players if p.name not in self.folded_players]) <= 1:
                    return

    def showdown(self):
        """Determines the winner(s) and distributes the pot."""
        print("\n--- SHOWDOWN ---")
        active_players = [player for player in self.players if player.name not in self.folded_players]
        if not active_players:
            print("Alle Spieler haben gefoldet. Pot bleibt unverteilt.")
            return

        community = self.community_cards
        player_hands = [(player, player.get_best_hand(community)) for player in active_players]

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
            print(f"Es gibt einen Split-Pot zwischen: {winner_names} mit {winner_info[0]}. Jeder erhält: {split_amount}")
            for winner in winners:
                winning_player = next(player for player in self.players if player.name == winner[0])
                winning_player.add_balance(split_amount)

    def declare_winner_if_only_one_remaining(self):
        """Checks if only one player remains and declares them the winner."""
        active_players = [player for player in self.players if player.name not in self.folded_players]
        if len(active_players) == 1:
            winner = active_players[0]
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

        for player in self.players:
            player.clear_cards()

        self.rotate_blinds()  # Move blinds to the next players

    def play_round(self):
        """Plays a complete round of poker, with option to modify settings before starting."""
        if input("Would you like to make any changes before starting the round? (yes/no): ").lower() == 'yes':
            self.modify_game_settings()

        display_spade_art()  # Display spade art on game start
        print("\n")
        display_new_round()
        self.assign_blinds()
        self.deal_private_cards()

        # Pre-Flop Betting
        self.betting_round('Pre-Flop')
        if self.declare_winner_if_only_one_remaining():
            self.reset_game()
            return

        # Flop
        self.deal_community_cards(3)
        self.betting_round('Flop')
        if self.declare_winner_if_only_one_remaining():
            self.reset_game()
            return

        # Turn
        self.deal_community_cards(1)
        self.betting_round('Turn')
        if self.declare_winner_if_only_one_remaining():
            self.reset_game()
            return

        # River
        self.deal_community_cards(1)
        self.betting_round('River')
        if self.declare_winner_if_only_one_remaining():
            self.reset_game()
            return

        # Showdown if more than one player remains
        self.showdown()
        self.reset_game()


def main():
    # Initialisiere Spieler
    player_names = ['Alice', 'Bob', 'Charlie', 'Diana']
    players = [Player(name) for name in player_names]

    # Initialisiere das Spiel
    game = GameRound(players, small_blind=10, big_blind=20)

    # Simuliere eine Pokerrunde
    game.play_round()


if __name__ == "__main__":
    main()
