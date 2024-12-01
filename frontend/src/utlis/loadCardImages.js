// src/utils/loadCardImages.js
const loadCardImages = () => {
  const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace'];
  const suits = ['hearts', 'diamonds', 'clubs', 'spades'];

  const images = {};

  // Load all the card images
  ranks.forEach(rank => {
    suits.forEach(suit => {
      images[`${rank}_${suit}`] = require(`card_deck/${rank}_of_${suit}.png`);
    });
  });

  // Add the backside of the card
  images['card_back'] = require('card_deck/card_backside.png');

  return images;
};

export default loadCardImages;
