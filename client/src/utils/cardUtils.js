export const loadCardImage = (rank, suit, faceUp = true) => {
  if (!faceUp) {
    return "images/card_deck/card_backside7.png"; // Path to the card backside image
  }
  return `images/card_deck/${rank}_of_${suit}.png`; // Card face image
};
