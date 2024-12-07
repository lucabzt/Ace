from server.src.game.resources.player import Player
from server.src.mediaplayer.sound_manager import play_player_action


def get_player_action(player, player_action_queue):
    """Determines the player's action. This is a placeholder for future AI integration."""
    action = player_action_queue.get()
    print(f"{player} {action}")

    if action == "fold":
        play_player_action(player, "fold")
        return "fold"
    elif action == "check":
        play_player_action(player, "check")
        return "check"
    elif action == "call":
        play_player_action(player, "call")
        return "call"
    elif action.startswith("raise"):
        _, raise_amount = action.split()
        raise_amount = int(raise_amount)
        play_player_action(player, "raise")
        return action
    else:
        print("Action Invalid.")


def modify_game_settings(game_round):
    """Allows the user to modify game settings or exit the game."""
    print("\n--- SETTINGS ---")
    print(
        "Options: 1) Add player, 2) Remove player, 3) Give balance to player, 4) Change blind sizes, 5) Continue, 6) Exit Game")
    choice = input("Choose an option (1-6): ")

    if choice == '1':
        player_name = input("Enter the new player's name: ")
        if player_name and player_name not in [player.name for player in game_round.players]:
            new_player = Player(player_name)
            game_round.players.append(new_player)
            game_round.bets[player_name] = 0
            print(f"Player {player_name} has been added.")
            game_round.reset_game()
        else:
            print("Invalid or duplicate player name.")

    elif choice == '2':
        player_name = input("Enter the player's name to remove: ")
        game_round.players = [player for player in game_round.players if player.name != player_name]
        if player_name in game_round.bets:
            del game_round.bets[player_name]
        game_round.reset_game()
        print(f"Player {player_name} has been removed.")

    elif choice == '3':
        player_name = input("Enter the player's name to give balance: ")
        player = next((p for p in game_round.players if p.name == player_name), None)
        if player:
            amount = int(input(f"Enter the amount to give to {player_name}: "))
            player.balance += amount
            print(f"{player_name} now has {player.balance} chips.")
            game_round.reset_game()
        else:
            print("Player not found.")

    elif choice == '4':
        game_round.small_blind = int(input("Enter new small blind: "))
        game_round.big_blind = int(input("Enter new big blind: "))
        game_round.reset_game()
        print(f"Blinds updated. Small Blind: {game_round.small_blind}, Big Blind: {game_round.big_blind}")

    elif choice == '5':
        print("Continuing without changes.")
    elif choice == '6':
        game_round.exit_game = True  # Set exit flag
        print("Exiting the game after this round.")
