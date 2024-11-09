import csv
from datetime import datetime


class Logger:
    def __init__(self):
        self.logs = []

    def log_round(self, round_name, pot, community_cards, player_bets, player_balances):
        log_entry = {
            'round': round_name,
            'pot': pot,
            'community_cards': [str(card) for card in community_cards],
            'player_bets': player_bets,
            'player_balances': player_balances
        }
        self.logs.append(log_entry)

    def save_logs(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"poker_game_log_{timestamp}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['round', 'pot', 'community_cards', 'player_bets', 'player_balances']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.logs:
                writer.writerow({
                    'round': entry['round'],
                    'pot': entry['pot'],
                    'community_cards': ', '.join(entry['community_cards']),
                    'player_bets': ', '.join([f"{k}: {v}" for k, v in entry['player_bets'].items()]),
                    'player_balances': ', '.join([f"{k}: {v}" for k, v in entry['player_balances'].items()])
                })
        print(f"Game log saved as {filename}.")
