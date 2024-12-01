// src/components/PokerTable.js
import React, { useState, useEffect } from 'react';
import Player from './Player';
import Pot from './Pot';
import DealerButton from './DealerButton';

const PokerTable = ({ players, communityCards, pot, dealerIndex }) => {
  const [foldedPlayers, setFoldedPlayers] = useState([]);

  useEffect(() => {
    // Handle any side-effects like changing round state or updating UI
  }, [foldedPlayers]);

  const getPlayerPosition = (index) => {
    const positions = [
      { x: 50, y: 450 }, // Player 1
      { x: 50, y: 50 }, // Player 2
      { x: 650, y: 40 }, // Player 3
      { x: 1250, y: 50 }, // Player 4
      { x: 1250, y: 450 }, // Player 5
      { x: 650, y: 700 }, // Player 6
    ];
    return positions[index];
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh', background: '#4b6f44' }}>
      <Pot pot={pot} />
      {players.map((player, index) => {
        const { x, y } = getPlayerPosition(index);
        return <Player key={index} player={player} x={x} y={y} folded={foldedPlayers.includes(player.name)} />;
      })}
      <div style={{ position: 'absolute', top: '50%', left: '50%' }}>
        {/* Render Community Cards */}
        <div style={{ display: 'flex', marginBottom: '20px' }}>
          {communityCards.map((card, index) => (
            <Card key={index} card={card} x={index * 95} y={0} />
          ))}
        </div>
      </div>
      <DealerButton x={getPlayerPosition(dealerIndex).x + 180} y={getPlayerPosition(dealerIndex).y + 70} />
    </div>
  );
};

export default PokerTable;
