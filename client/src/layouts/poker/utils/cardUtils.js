// Function to load a card image based on rank, suit, and whether the card is face-up or face-down
export const loadCardImage = (rank, suit, faceUp = true) => {
  if (!faceUp) {
    // Dynamically require the backside image
    return require("../../../assets/images/poker/card_deck/card_backside7.png");
  }

  try {
    // Dynamically require the card face image based on rank and suit
    return require(`../../../assets/images/poker/card_deck/${rank.toLowerCase()}_of_${suit.toLowerCase()}.png`);
  } catch (error) {
    console.error(`Error loading image for ${rank} of ${suit}:`, error);
    // Optional: Provide a fallback, like the backside image
    return require("../../../assets/images/poker/card_deck/card_backside7.png");
  }
};