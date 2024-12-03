from src.game.utils.game_utils import evaluate_hand, tie_breaker, translate_winner_hands


class WinnerAnalyzer:
    def __init__(self, players):
        self.players = players  # List of tuples (player_name, player_cards)

    def analyze_winners(self):
        """
        Analyzes all players' hands and determines the winner(s) based on the best hand.
        Handles tie situations by returning all players with the best hand.

        :return: A list of tuples containing player names and their best hands.
        """
        winners = []
        best_hand = None
        best_hand_type = None

        # Loop through each player in the array
        for player_name, player_cards in self.players:
            hand_type, attr = evaluate_hand(player_cards)

            if best_hand_type is None or hand_type < best_hand_type:
                best_hand_type = hand_type
                best_hand = (sorted(player_cards), attr)

                winners.clear()
                winners.append((player_name, best_hand_type, best_hand))

            elif hand_type == best_hand_type:
                best_combination, best_attr = best_hand  # Unpack properly

                temp = best_hand
                best_hand, split_pot = tie_breaker(hand_type, sorted(player_cards), attr, best_attr, best_hand)

                if split_pot:
                    winners.append((player_name, best_hand_type, best_hand))
                elif temp != best_hand:
                    best_hand_type = hand_type
                    best_hand = (sorted(player_cards), attr)

                    winners.clear()
                    winners.append((player_name, best_hand_type, best_hand))

        winners = translate_winner_hands(winners)

        return winners
