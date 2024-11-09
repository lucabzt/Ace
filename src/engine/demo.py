from table import Engine

holdem_game = Engine(num_players=5, deck_type='full')
holdem_game.add_to_hand(1, ['Td', 'Ts'])
holdem_game.add_to_hand(2, ['5d', 'As'])
holdem_game.next_round()
holdem_game.next_round()
print(holdem_game.view_table())
print(holdem_game.simulate())