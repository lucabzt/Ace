import pygame
import os
from src.game.game_round.game_round import GameRound
from src.game.resources.player import Player

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

# Initialize pygame screen with new dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Poker Game")

# Font settings
FONT = pygame.font.Font(None, 32)  # Slightly smaller font for more players


class VisualGameRound(GameRound):
    def __init__(self, players, small_blind, big_blind):
        super().__init__(players, small_blind, big_blind)
        self.card_images = self.load_card_images()
        self.background_image = self.load_background_image()
        self.round_step = 0

    def play_round_with_display(self):
        """Run the poker game one step at a time for visual updates."""
        if self.round_step == 0:
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

        # Update display and increment the step
        self.update_display()
        self.round_step += 1

    def load_card_images(self):
        image_path = "/Users/sebastianrogg/PycharmProjects/Spade/images/card_deck"
        images = {}
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']

        for rank in ranks:
            for suit in suits:
                image_name = f"{rank}_of_{suit}.png"
                full_path = os.path.join(image_path, image_name)
                try:
                    # Load and resize the image to 60x90
                    card_image = pygame.image.load(full_path)
                    card_image = pygame.transform.scale(card_image, (60, 90))
                    images[f"{rank}_{suit}"] = card_image
                except pygame.error:
                    print(f"Image {full_path} not found.")
        return images

    def load_background_image(self):
        try:
            bg_image = pygame.image.load("/path/to/background_image.jpg")  # Replace with actual path
            return pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Background image not found.")
            return None

    def display_cards(self, cards, x, y):
        for i, card in enumerate(cards):
            card_key = f"{card.rank.value.lower()}_{card.suit.value.lower()}"
            card_image = self.card_images.get(card_key)
            if card_image:
                screen.blit(card_image, (x + i * 70, y))  # Adjusted spacing for readability
            else:
                placeholder_text = FONT.render("?", True, WHITE)
                screen.blit(placeholder_text, (x + i * 70, y))

    def display_community_cards(self):
        self.display_cards(self.community_cards, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100)

    def display_player_cards(self, player, x, y):
        self.display_cards(player.cards, x, y)

    def display_pot(self):
        pot_text = FONT.render(f"Pot: {self.pot}", True, WHITE)
        screen.blit(pot_text, (SCREEN_WIDTH // 2 - pot_text.get_width() // 2, SCREEN_HEIGHT - 100))

    def display_player_info(self):
        positions = [
            (50, SCREEN_HEIGHT - 150),       # Player 1
            (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 150),  # Player 2
            (50, 50),                         # Player 3
            (SCREEN_WIDTH - 250, 50),         # Player 4
            (SCREEN_WIDTH // 2 - 150, 50),    # Player 5 - Center top
            (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 150)  # Player 6 - Center bottom
        ]

        for i, player in enumerate(self.players):
            x, y = positions[i]
            self.display_player_cards(player, x, y)
            player_text = FONT.render(f"{player.name}: {self.bets[player.name]} Chips", True, WHITE)
            screen.blit(player_text, (x, y - 30))

    def update_display(self):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(GREEN)  # Fallback color

        self.display_community_cards()
        self.display_pot()
        self.display_player_info()
        pygame.display.flip()


# Function to run the game loop
def main():
    # Initialize the players and the game round
    player_names = ['Markus', 'Jonas', 'Luca', 'Paul', 'Sebastian', 'Anna']
    players = [Player(name) for name in player_names]
    game = VisualGameRound(players, small_blind=10, big_blind=20)

    # Main game loop
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
