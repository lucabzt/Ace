def get_player_action(player, to_call):
    """Determines the player's action. This is a placeholder for future AI integration."""
    while True:
        print(f"\n{player.name}, dein Zug:")
        print(f"Betrag zum Callen: {to_call}")
        action = input("Wähle eine Aktion (check, call, fold, raise <amount>): ").strip().lower()

        if action == "fold":
            return "fold"
        elif action == "check":
            return "check"
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
            print("Ungültige Aktion. Bitte gib 'check', 'call', 'fold' oder 'raise <Betrag>' ein.")

