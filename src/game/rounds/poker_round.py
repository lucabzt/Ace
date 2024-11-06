from src.game.hand_analysis.winner_determiner import WinnerAnalyzer
from src.game.resources.player import Player
from src.game.resources.poker_deck import Deck


class GameRound:
    def __init__(self, players, small_blind, big_blind):
        """
        Initialisiert das Spiel mit den angegebenen Spielern und Blinds.

        :param players: Liste von Player-Objekten
        :param small_blind: Betrag des Small Blinds
        :param big_blind: Betrag des Big Blinds
        """
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

    def assign_blinds(self):
        """Weist den Small und Big Blind den entsprechenden Spielern zu."""
        self.small_blind_player = self.players[0]
        self.big_blind_player = self.players[1]
        # Setzen der Blinds
        self.pot += self.small_blind + self.big_blind
        self.bets[self.small_blind_player.name] += self.small_blind
        self.bets[self.big_blind_player.name] += self.big_blind
        self.current_bet = self.big_blind
        print(f"{self.small_blind_player.name} setzt Small Blind: {self.small_blind}")
        print(f"{self.big_blind_player.name} setzt Big Blind: {self.big_blind}")

    def deal_private_cards(self):
        """Verteilt zwei Karten an jeden Spieler."""
        for _ in range(2):
            for player in self.players:
                card = self.deck.deal_card()
                player.receive_card(card)
                print(f"{player.name} erhält Karte: {card}")

    def betting_round(self, round_name):
        """
        Führt eine Setzrunde durch.

        :param round_name: Name der Setzrunde (z.B. 'Pre-Flop', 'Flop', etc.)
        """
        print(f"\n--- {round_name} ---")
        active_players = [player for player in self.players if player.name not in self.folded_players]

        for player in active_players:
            active_players = [player for player in self.players if player.name not in self.folded_players]
            if len(active_players) == 1:
                continue
            action = self.get_player_action(player, self.current_bet - self.bets[player.name])
            if action == 'fold':
                self.folded_players.add(player.name)
                print(f"{player.name} foldet.")
            elif action == 'call':
                call_amount = self.current_bet - self.bets[player.name]
                self.pot += call_amount
                self.bets[player.name] += call_amount
                print(f"{player.name} callt: {call_amount}")
            elif action.startswith('raise'):
                _, raise_amount = action.split()
                raise_amount = int(raise_amount)
                total_bet = self.current_bet - self.bets[player.name] + raise_amount
                self.pot += total_bet
                self.bets[player.name] += total_bet
                self.current_bet += raise_amount
                print(f"{player.name} raiset um: {raise_amount}")
            # Weitere Aktionen wie 'check' können hinzugefügt werden

    def get_player_action(self, player, to_call):
        """
        Bestimmt die Aktion eines Spielers. Hier können Sie die Interaktion mit der AI einfügen.
        Derzeit wird die Aktion zufällig gewählt.

        :param player: Player-Objekt
        :param to_call: Betrag, den der Spieler callen muss
        :return: Aktion als String
        """
        # Platzhalter für AI-Integration. Hier wird zufällig entschieden.
        while True:
            print(f"\n{player.name}, dein Zug:")
            print(f"Betrag zum Callen: {to_call}")
            action = input("Wähle eine Aktion (fold, call, raise <amount>): ").strip().lower()

            # Validate input format
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
        """
        Fügt Gemeinschaftskarten hinzu.

        :param number: Anzahl der zu dealenden Gemeinschaftskarten
        """
        for _ in range(number):
            card = self.deck.deal_card()
            self.community_cards.append(card)
            print(f"Gemeinschaftskarte: {card}")

    def showdown(self):
        """Ermittelt und zeigt die Gewinner an."""
        print("\n--- Showdown ---")
        active_players = [player for player in self.players if player.name not in self.folded_players]
        if not active_players:
            print("Alle Spieler haben gefoldet. Pot bleibt unverteilt. WTF")
            return
        # Annahme: community_cards sind bereits gesetzt
        community = self.community_cards
        player_hands = []

        for player in active_players:
            best_hand = player.get_best_hand(community)
            player_hands.append(
                (player.name, best_hand[0], best_hand[1]))  # Store the player's name, hand type, and cards

        # Print each player's best hand
        for player_name, hand_type, best_hand in player_hands:
            print(f"{player_name}'s Best Hand: {hand_type} with cards {sorted(best_hand)}")

        # To find winners, you would integrate this with WinnerAnalyzer
        analyzer = WinnerAnalyzer([(player_name, best_hand) for player_name, _, best_hand in player_hands])
        winners = analyzer.analyze_winners()


        if len(winners) == 1:
            winner = winners[0]
            print("")
            print(f"Gewinner ist {winner[0]} mit {winner[1]}. Pot: {self.pot}")
        else:
            winner_names = ', '.join([winner[0] for winner in winners])
            print(f"Es gibt einen Split-Pot zwischen: {winner_names}. Pot: {self.pot}")

    def declare_winner_if_only_one_remaining(self):
        """Überprüft, ob nur noch ein Spieler übrig ist und erklärt diesen als Gewinner."""
        active_players = [player for player in self.players if player.name not in self.folded_players]
        if len(active_players) == 1:
            # Wenn nur ein Spieler übrig ist, wird dieser als Gewinner erklärt
            winner = active_players[0]
            print(f"{winner.name} gewinnt, da alle anderen Spieler gefoldet haben.")
            return True
        return False

    def reset_game(self):
        """Setzt das Spiel für die nächste Runde zurück."""
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.bets = {player.name: 0 for player in self.players}
        self.folded_players = set()
        for player in self.players:
            player.clear_cards()

    def play_round(self):
        """Spielt eine vollständige Pokerrunde."""
        self.assign_blinds()
        self.deal_private_cards()

        # Pre-Flop Betting
        self.betting_round('Pre-Flop')
        if self.declare_winner_if_only_one_remaining():
            self.reset_game()
            return  # Runde endet, da nur noch ein Spieler übrig ist

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
