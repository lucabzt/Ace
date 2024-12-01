// src/components/Card.js
import React from 'react';

const Card = ({ card, x, y, isFolded }) => {
  const cardImages = require('../utils/loadCardImages').default();
  const cardKey = `${card.rank}_${card.suit}`;
  const image = cardImages[cardKey];

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: isFolded ? 'grayscale(100%)' : 'none',
        transition: 'all 0.2s ease',
      }}
    >
      <img src={image} alt={`${card.rank} of ${card.suit}`} width={90} height={131} />
    </div>
  );
};

export default Card;
