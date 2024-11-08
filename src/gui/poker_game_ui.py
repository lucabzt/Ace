import os

import pygame

from src.game.resources.player import Player
from src.game.rounds.poker_round import GameRound, display_spade_art, display_new_round

PATH_TO_SPADE = "/Users/sebastianrogg/PycharmProjects/Spade"

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1200
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


class poker_game_ui(GameRound):
    def __init__(self, players, small_blind, big_blind):
        super().__init__(players, small_blind, big_blind)
        self.card_images = self.load_card_images()
        self.background_image = self.load_background_image()
        self.round_step = 0
        display_spade_art()  # Display spade art on game start

    def play_round_with_display(self):
        """Run the poker game one step at a time for visual updates."""
        if self.round_step == 0:
            display_new_round()
            self.assign_blinds()
            self.deal_private_cards()
        elif self.round_step == 1:
            self.betting_round("Pre-Flop")
        elif self.round_step == 2:
            self.deal_community_cards(3)  # Deal the Flop
        elif self.round_step == 3:
            self.betting_round("Flop")
        elif self.round_step == 4:
            self.deal_community_cards(1)  # Deal the Turn
        elif self.round_step == 5:
            self.betting_round("Turn")
        elif self.round_step == 6:
            self.deal_community_cards(1)  # Deal the River
        elif self.round_step == 7:
            self.betting_round("River")
        elif self.round_step == 8:
            self.showdown()
            self.round_step = -1  # Reset for the next round
            self.reset_game()

        # Update display and increment the step
        self.update_display()
        self.round_step += 1

    def load_card_images(self):
        image_path = os.path.join(PATH_TO_SPADE, "assets/images/card_deck")
        images = {}
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']

        for rank in ranks:
            for suit in suits:
                image_name = f"{rank}_of_{suit}.png"
                full_path = os.path.join(image_path, image_name)
                try:
                    # Load and resize the image to 90x131
                    card_image = pygame.image.load(full_path)
                    card_image = pygame.transform.scale(card_image, (90, 131))
                    images[f"{rank}_{suit}"] = card_image
                except pygame.error:
                    print(f"Image {full_path} not found.")
        return images

    def load_background_image(self):
        try:
            bg_image = pygame.image.load(os.path.join(PATH_TO_SPADE, "assets/images/PokerTable.png"))
            return pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Background image not found.")
            return None

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
        is_folded = player.name in self.folded_players
        for i, card in enumerate(player.cards):
            card_key = f"{card.rank.value.lower()}_{card.suit.value.lower()}"
            card_image = self.card_images.get(card_key)
            if card_image:
                # Apply grayscale effect if player has folded
                if is_folded:
                    card_image = self.apply_grayscale(card_image)
                screen.blit(card_image, (x + i * 95, y))  # Increased space for larger cards
            else:
                placeholder_text = FONT.render("?", True, WHITE)
                screen.blit(placeholder_text, (x + i * 95, y))

    def apply_grayscale(self, image):
        grayscale_image = pygame.Surface(image.get_size())
        grayscale_image.blit(image, (0, 0))

        grayscale_image.lock()
        for x in range(grayscale_image.get_width()):
            for y in range(grayscale_image.get_height()):
                red, green, blue, alpha = grayscale_image.get_at((x, y))
                gray = int(0.3 * red + 0.59 * green + 0.11 * blue)
                grayscale_image.set_at((x, y), (gray, gray, gray, alpha))
        grayscale_image.unlock()

        return grayscale_image

    def display_pot(self):
        pot_text = FONT.render(f"Pot: {self.pot}", True, WHITE)
        screen.blit(pot_text, (SCREEN_WIDTH // 2 - pot_text.get_width() // 2, SCREEN_HEIGHT - 350))

    def display_player_info(self):
        positions = [
            (50, SCREEN_HEIGHT - 350),  # Player 1
            (50, 50),  # Player 2
            (SCREEN_WIDTH // 2 - 100, 20),  # Player 3 - Center top
            (SCREEN_WIDTH - 290, 50),  # Player 4
            (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 350),  # Player 5
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200)  # Player 6 - Center bottom
        ]

        for i, player in enumerate(self.players):
            x, y = positions[i]
            self.display_player_cards(player, x, y)

            # Check if player is folded and set text color accordingly
            is_folded = player.name in self.folded_players
            text_color = RED if is_folded else WHITE

            # Render player name and current bet in the chosen color
            player_text = FONT.render(f"{player.name}: {self.bets[player.name]} Chips", True, text_color)
            screen.blit(player_text, (x, y + 140))

            # Render player balance below the bet information
            balance_text = FONT.render(f"Balance: {player.balance} Chips", True, WHITE)
            screen.blit(balance_text, (x, y + 170))

    def update_display(self):
        if self.background_image:
            screen.fill((112, 4, 52))
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((75, 0, 130))

        self.display_community_cards()
        self.display_pot()
        self.display_player_info()
        pygame.display.flip()


# Function to run the game loop
def main():
    player_names = ['Jonas', 'Markus', 'Luca', 'Matthi', 'Sebastian', 'Paul']
    players = [Player(name) for name in player_names]
    game = poker_game_ui(players, small_blind=10, big_blind=20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.play_round_with_display()
        pygame.display.flip()
        pygame.time.delay(500)

    pygame.quit()


if __name__ == "__main__":
    main()
