import os

import pygame


def load_card_images():
    from src.gui.poker_game_ui import PATH_TO_SPADE, SCREEN_WIDTH, SCREEN_HEIGHT
    image_path = os.path.join(PATH_TO_SPADE, "assets/images/card_deck")
    images = {}
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']

    for rank in ranks:
        for suit in suits:
            image_name = f"{rank}_of_{suit}.png"
            full_path = os.path.join(image_path, image_name)
            try:
                # Load the image at its original resolution
                card_image = pygame.image.load(full_path)

                # Resize the image to 90x131
                resized_image = pygame.transform.smoothscale(card_image, (90, 131))
                images[f"{rank}_{suit}"] = resized_image
            except pygame.error:
                print(f"Image {full_path} not found.")

    return images


def load_background_image():
    from src.gui.poker_game_ui import PATH_TO_SPADE, SCREEN_WIDTH, SCREEN_HEIGHT
    try:
        bg_image = pygame.image.load(os.path.join(PATH_TO_SPADE, "assets/images/PokerTable4.png"))
        return pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print("Background image not found.")
        return None


def load_dealer_button():
    from src.gui.poker_game_ui import PATH_TO_SPADE, SCREEN_WIDTH, SCREEN_HEIGHT
    try:
        button_image = pygame.image.load(os.path.join(PATH_TO_SPADE, "assets/images/DealerButton.png"))
        return pygame.transform.scale(button_image, (40, 40))  # Adjust size as needed
    except pygame.error:
        print("Dealer button image not found.")
        return None


def apply_grayscale(image):
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
