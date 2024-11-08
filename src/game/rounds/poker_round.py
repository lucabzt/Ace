from src.game.hand_analysis.winner_determiner import WinnerAnalyzer
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

    def display_spade_art(self):
        """Displays Spade ASCII art on game startup."""
        spade_art = """
                          /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$
                         /$$__  $$| $$__  $$ /$$__  $$| $$__  $$| $$_____/
                        | $$  \__/| $$  \ $$| $$  \ $$| $$  \ $$| $$      
                        |  $$$$$$ | $$$$$$$/| $$$$$$$$| $$  | $$| $$$$$   
                         \____  $$| $$____/ | $$__  $$| $$  | $$| $$__/   
                         /$$  \ $$| $$      | $$  | $$| $$  | $$| $$      
                        |  $$$$$$/| $$      | $$  | $$| $$$$$$$/| $$$$$$$$
                         \______/ |__/      |__/  |__/|_______/ |________/
                                                  
            ---------- # ------------------------------------------------------------------
            --------- ##= ------------------------------ Exmatrikulation ------------------
            -------- ##=== ------------------ Luca, Markus, Sebi, Jonas, Paul, Matthi -----
            ------ ###==#=== --------------------------------------------------------------
            ---- ####===##==== ------------------------------------------------------------
            -- #####====###===== ------      "My name is Spade...                     -----
            - #####=====####===== -----       I am you AI Poker Dealer...             -----
            - #####=====####===== -----       Prepare to play!"                       -----
            --- ####=  #  #==== ------- - My little programmer (Markus Huber)         -----
            --------- ##= -----------------------------------------------------------------
            ------- ####=== ---------------------------------------------------------------                               
        
        """
        print(spade_art)

    def display_new_round(self):
        new_round = """
                ♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠  .------..------..------..------..------.
                ♠                               ♠  |S.--. ||P.--. ||A.--. ||D.--. ||E.--. |
                ♠           NEW ROUND!          ♠  | :/\: || :/\: || (\/) || :/\: || (\/) |
                ♠           NEW LUCK!           ♠  | :\/: || (__) || :\/: || (__) || :\/: |
                ♠                               ♠  | '--'S|| '--'P|| '--'A|| '--'D|| '--'E|
                ♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠♠  `------'`------'`------'`------'`------´
                """
        print(new_round)

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

        while not all(players_in_round[player.name] for player in active_players if player.name not in self.folded_players):
            for player in player_order:
                if player.name in self.folded_players:
                    continue  # Skip folded players

                # Skip if this is the player who last raised and everyone else has called or folded
                if last_raiser == player.name and all(players_in_round[p.name] for p in active_players if p.name not in self.folded_players):
                    return  # End betting round

                to_call = self.current_bet - self.bets[player.name]
                action = self.get_player_action(player, to_call)

                if action == 'fold':
                    self.folded_players.add(player.name)
                    print(f"{player.name} folds.")
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

    def get_player_action(self, player, to_call):
        """Determines the player's action. This is a placeholder for future AI integration."""
        while True:
            print(f"\n{player.name}, dein Zug:")
            print(f"Betrag zum Callen: {to_call}")
            action = input("Wähle eine Aktion (fold, call, raise <amount>): ").strip().lower()

            if action == "fold":
                return "fold"
            elif action == "call":
                return "call"
            elif action.startswith("raise"):
                try:
                    _, raise_amount = action.split()
                    raise_amount = int(raise_amount)
                    if raise_amount > 0:
                        return f"raise {raise_amount}"
                    else:
                        print("Der Raise-Betrag muss positiv sein.")
                except ValueError:
                    print("Ungültiger Betrag für Raise.")
            else:
                print("Ungültige Aktion. Bitte gib 'fold', 'call' oder 'raise <Betrag>' ein.")

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
            split_amount = self.pot // len(winners)
            winner_names = ', '.join([winner[0] for winner in winners])
            print(f"Es gibt einen Split-Pot zwischen: {winner_names}. Jeder erhält: {split_amount}")
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
        """Plays a complete round of poker."""
        self.display_spade_art()  # Display spade art on game start
        print("\n")
        self.display_new_round()
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
