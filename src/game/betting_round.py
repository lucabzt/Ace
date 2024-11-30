from src.game.input import get_player_action
from src.mediaplayer.sound_manager import play_community_card_sound


class BettingRound:
    def __init__(self, players, pot, current_bet, small_blind_index, folded_players, active_players, bets,
                 update_display):
        self.players = players
        self.pot = pot
        self.current_bet = current_bet
        self.small_blind_index = small_blind_index
        self.folded_players = folded_players
        self.active_players = active_players
        self.bets = bets
        self.last_raiser = None  # Keeps track of the last player to raise
        self.players_in_round = {player.name: False for player in self.active_players}
        self.update_display = update_display  # Store the reference to the update_display method

    def execute(self, round_name):
        """Executes a betting round with players matching, raising, or folding as needed."""
        print(f"\n--- {round_name.upper()} BETTING ---")

        # Dealer voice line
        play_community_card_sound(round_name)

        # Determine the starting player for the betting round
        if round_name == 'Pre-Flop':
            start_index = (self.small_blind_index + 2) % len(self.players)
        else:
            start_index = self.small_blind_index

        player_order = self.active_players[start_index:] + self.active_players[:start_index]

        # Track which players have matched the current bet
        players_in_round = {player.name: False for player in self.active_players}
        last_raiser = None

        while not all(
                players_in_round[player.name] for player in self.active_players if player not in self.folded_players):

            for player in player_order:
                if player in self.folded_players:
                    continue  # Skip folded players

                # Skip if this is the player who last raised and everyone else has called or folded
                if last_raiser == player.name and all(
                        players_in_round[p.name] for p in self.active_players if p not in self.folded_players):
                    return  # End betting round

                to_call = self.current_bet - self.bets[player.name]

                while True:
                    action = get_player_action(player, to_call)  # TODO: AI ACTION GETTER

                    if action == 'fold':
                        player.win_prob = 0.
                        self.folded_players.add(player)
                        self.active_players.remove(player)
                        print(f"{player.name} folds.")
                        self.update_display()  # Update display after fold
                        break
                    elif action == 'check':
                        call_amount = to_call
                        if call_amount == 0:
                            players_in_round[player.name] = True
                            print(f"{player.name} checks")
                            self.update_display()  # Update display after check
                            break
                        else:
                            print(f"Can't check! {player.name} has to call: {call_amount}/raise/fold!")
                            continue
                    elif action == 'call':
                        call_amount = to_call
                        if player.balance >= call_amount:
                            player.balance -= call_amount
                            self.bets[player.name] += call_amount
                            self.pot += call_amount
                            players_in_round[player.name] = True
                            print(f"{player.name} calls: {call_amount}")
                            self.update_display()  # Update display after call
                            break
                        else:
                            print(f"{player.name} does not have enough chips to call. Please choose another action.")
                            continue
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
                            players_in_round = {p.name: (p in self.folded_players) for p in self.active_players}
                            players_in_round[player.name] = True  # Player who raised has already matched their own bet
                            self.update_display()  # Update display after raise
                            break
                        else:
                            print(f"{player.name} does not have enough chips to raise. Please choose another action.")
                            continue

                # Break if only one active player remains
                if len([p for p in self.active_players if p not in self.folded_players]) <= 1:
                    return
