import React, { useState, useEffect } from "react";
import Player from "../Player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";
import { players } from "../../data/playersData";  // Import players data
import { communityCards } from "../../data/communityCardsData";  // Import community cards data

const PokerGameUI = () => {
  const pot = 500;
  const dealerIndex = 2; // First player is the dealer
  const pokerTableBackground = "PokerTable100.png"; // Path to table image

  const [playerPositions, setPlayerPositions] = useState(getPlayerPositions(players.length));

  // Recalculate player positions on window resize
  useEffect(() => {
    const handleResize = () => {
      setPlayerPositions(getPlayerPositions(players.length));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [players.length]);

  return (
    <PokerTable pokerTableBackground={pokerTableBackground} pot={pot}>
      {players.map((player, index) => {
        const position = playerPositions[index];
        const isDealer = index === dealerIndex;
        return (
          <Player
            key={index}
            player={player}
            position={position}
            isDealer={isDealer}
          />
        );
      })}

      {/* Community Cards */}
      <div
        style={{
          position: "absolute",
          top: "45%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          gap: "1vw",  // Responsive gap between community cards
        }}
      >
        {communityCards.map((card, index) => (
          <img
            key={index}
            src={loadCardImage(card.rank, card.suit, card.faceUp)}
            alt={`${card.rank} of ${card.suit}`}
            style={{
              width: "6vw",  // Responsive size for community cards
              height: "auto",
            }}
          />
        ))}
      </div>
    </PokerTable>
  );
};

export default PokerGameUI;
