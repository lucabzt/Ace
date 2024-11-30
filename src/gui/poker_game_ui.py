from pathlib import Path

import pygame

from src.game.betting_round import BettingRound
from src.game.input import modify_game_settings
from src.game.resources.player import Player
from src.game.game_round import GameRound, display_new_round
from src.game.utils.game_utils import display_spade_art
from src.gui.gui_loader import load_card_images, load_background_image, load_dealer_button, apply_grayscale

# Path setup
BASE_DIR = base_path = Path(__file__).resolve().parent.parent.parent  # Go up three directories from mediaplayer
PATH_TO_SPADE = BASE_DIR

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)

# Initialize pygame screen with fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poker Game")

# Font settings
FONT = pygame.font.Font(None, 32)  # Slightly smaller font for more players


def get_player_position(index):
    positions = [
        (50, SCREEN_HEIGHT - 350),  # Player 1
        (50, 50),  # Player 2
        (SCREEN_WIDTH // 2 - 100, 40),  # Player 3 - Center top
        (SCREEN_WIDTH - 290, 50),  # Player 4
        (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 350),  # Player 5
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200)  # Player 6 - Center bottom
    ]
    return positions[index % len(positions)]


class poker_game_ui(GameRound):
    def __init__(self, players, small_blind, big_blind):
        super().__init__(players, small_blind, big_blind)
        self.card_images = load_card_images()
        self.background_image = load_background_image()
        self.dealer_button = load_dealer_button()
        self.round_step = 0

    def play_round_with_display(self):
        """Plays a complete round of poker, with option to modify settings before starting."""
        """Run the poker game one step at a time for visual updates."""

        betting_round = BettingRound(self.players, self.pot, self.current_bet, self.small_blind_index,
                                     self.folded_players, self.active_players, self.bets)

        if self.round_step == 0:
            if input("Would you like to make any changes before starting the round? (yes/no): ").lower() == 'yes':
                modify_game_settings(self)  # Use the input module's method
                if self.exit_game:
                    self.save_logs()
                    print("Game exited.")
                    return  # Exit game if user chose to

            display_new_round()
            self.assign_blinds()
            self.deal_private_cards()
            print("---------------")
            self.calculate_probabilities()
        elif self.round_step == 1:
            betting_round.execute('Pre-Flop')
            self.log_round('Pre-Flop')  # Log after each round
            if self.declare_winner_if_only_one_remaining():
                self.prep_next_round()

        elif self.round_step == 2:
            self.deal_community_cards(3)  # Deal the Flop

            self.calculate_probabilities()

        elif self.round_step == 3:
            betting_round.execute("Flop")
            self.log_round('Flop')  # Log after each round
            if self.declare_winner_if_only_one_remaining():
                self.prep_next_round()

        elif self.round_step == 4:
            self.deal_community_cards(1)  # Deal the Turn

            self.calculate_probabilities()

        elif self.round_step == 5:
            betting_round.execute("Turn")
            self.log_round('Turn')  # Log after each round
            if self.declare_winner_if_only_one_remaining():
                self.prep_next_round()

        elif self.round_step == 6:
            self.deal_community_cards(1)  # Deal the River
            self.calculate_probabilities(True)

        elif self.round_step == 7:
            betting_round.execute("River")
            self.log_round('River')  # Log after each round

        elif self.round_step == 8:
            self.showdown()
            self.prep_next_round()

        # Update display and increment the step
        self.update_display()
        self.round_step += 1

    def prep_next_round(self):
        self.round_step = -1  # Reset for the next round
        self.reset_game()

    def display_cards(self, cards, x, y):
        for i, card in enumerate(cards):
            card_key = f"{card.rank.value.lower()}_{card.suit.value.lower()}"
            card_image = self.card_images.get(card_key)
            if card_image:
                # Adjusted spacing for the new card size
                screen.blit(card_image, (x + i * 95, y))  # Slightly more space between cards
            else:
                placeholder_text = FONT.render("?", True, WHITE)
                screen.blit(placeholder_text, (x + i * 95, y))

    def display_community_cards(self):
        # Adjusted position for the larger cards to keep centered
        self.display_cards(self.community_cards, SCREEN_WIDTH // 2 - 235, SCREEN_HEIGHT // 2 - 100)

    def display_player_cards(self, player, x, y):
        """Displays player cards. If the player has folded, the cards are displayed in grayscale."""
        is_folded = (player in self.folded_players)
        for i, card in enumerate(player.cards):
            card_key = f"{card.rank.value.lower()}_{card.suit.value.lower()}"
            card_image = self.card_images.get(card_key)
            if card_image:
                # Apply grayscale effect if player has folded
                if is_folded:
                    card_image = apply_grayscale(card_image)
                screen.blit(card_image, (x + i * 95, y))  # Increased space for larger cards
            else:
                placeholder_text = FONT.render("?", True, WHITE)
                screen.blit(placeholder_text, (x + i * 95, y))

    def display_pot(self):
        pot_text = FONT.render(f"Pot: {self.pot}", True, WHITE)
        screen.blit(pot_text, (SCREEN_WIDTH // 2 - pot_text.get_width() // 2, SCREEN_HEIGHT - 350))

    def display_player_info(self):
        positions = [
            (50, SCREEN_HEIGHT - 350),  # Player 1
            (50, 50),  # Player 2
            (SCREEN_WIDTH // 2 - 100, 40),  # Player 3 - Center top
            (SCREEN_WIDTH - 290, 50),  # Player 4
            (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 350),  # Player 5
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200)  # Player 6 - Center bottom
        ]

        for i, player in enumerate(self.players):
            x, y = positions[i]

            # Render player name and win probability
            name_prob_text = FONT.render(f"{player.name}: {player.win_prob:.2f}%", True, WHITE)
            name_prob_rect = name_prob_text.get_rect(centerx=x + 100, top=y - 35)
            screen.blit(name_prob_text, name_prob_rect)

            # Display cards
            self.display_player_cards(player, x + 5, y)

            # Check if player is folded and set text color accordingly
            is_folded = player in self.folded_players
            text_color = RED if is_folded else WHITE

            # Render current bet
            bet_text = FONT.render(f"{self.bets[player.name]} Chips", True, text_color)
            bet_rect = bet_text.get_rect(centerx=x + 100, top=y + 140)
            screen.blit(bet_text, bet_rect)

            # Render player balance
            balance_text = FONT.render(f"Balance: {player.balance}", True, WHITE)
            balance_rect = balance_text.get_rect(centerx=x + 100, top=y + 170)
            screen.blit(balance_text, balance_rect)

    def display_dealer_button(self):
        if self.dealer_button:
            x, y = get_player_position(self.dealer_index)
            screen.blit(self.dealer_button, (x + 180, y + 70))  # Adjust position as needed

    def update_display(self):
        # Check if there's a background image. If not, set a purple background.
        if self.background_image:
            screen.fill((112, 4, 52))  # Fill with a darker purple
            screen.blit(self.background_image, (0, 0))  # Draw background image
        else:
            screen.fill((128, 0, 128))  # A medium purple if no image is loaded

        # Draw community cards, pot, and player info
        self.display_community_cards()
        self.display_pot()
        self.display_player_info()
        self.display_dealer_button()

        # Update the display with all changes
        pygame.display.flip()


# Function to run the game loop
def main():
    player_names = ['Hoerter', 'Rogg', 'Bozzetti', 'Vorderbruegge', 'Huber', 'Meierlohr']
    players = [Player(name) for name in player_names]
    game = poker_game_ui(players, small_blind=10, big_blind=20)

    running = True
    clock = pygame.time.Clock()  # Control the frame rate

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.play_round_with_display()
        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    main()
