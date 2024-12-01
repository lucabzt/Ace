// src/components/Player.js
import React from 'react';
import Card from './Card';

const Player = ({ player, x, y, folded }) => {
  return (
    <div style={{ position: 'absolute', left: x, top: y }}>
      <h3>{player.name}</h3>
      <p>Balance: {player.balance}</p>
      <p>Bet: {player.bet}</p>
      <div style={{ display: 'flex' }}>
        {player.cards.map((card, index) => (
          <Card key={index} card={card} x={x + 5 + index * 95} y={y} isFolded={folded} />
        ))}
      </div>
    </div>
  );
};

export default Player;
