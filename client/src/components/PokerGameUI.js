import React, { useState } from "react";

const loadCardImage = (rank, suit, faceUp = true) => {
  if (!faceUp) {
    return 'card_deck/card_backside7.png'; // Path to the card backside image
  }
  return `card_deck/${rank}_of_${suit}.png`;
};

const getPlayerPositions = (numPlayers) => {
  const radiusX = window.innerWidth / 2.5;
  const radiusY = window.innerHeight / 2.7;
  const centerX = window.innerWidth / 2 - 20;
  const centerY = window.innerHeight / 2 + 40;

  return Array.from({ length: numPlayers }, (_, i) => {
    const angle = (2 * Math.PI * i) / numPlayers;
    return {
      x: centerX + radiusX * Math.cos(angle),
      y: centerY + radiusY * Math.sin(angle),
    };
  });
};

const PokerGameUI = () => {
  const [players, setPlayers] = useState([
    {
      name: "Player 1",
      probWin: "75%",
      balance: 1000,
      bet: 50,
      cards: [
        { rank: "ace", suit: "hearts", faceUp: true }, // Face-up card
        { rank: "king", suit: "hearts", faceUp: false }, // Face-down card
      ],
    },
    {
      name: "Player 2",
      probWin: "60%",
      balance: 950,
      bet: 30,
      cards: [
        { rank: "queen", suit: "diamonds", faceUp: true },
        { rank: "jack", suit: "diamonds", faceUp: true },
      ],
    },
    {
      name: "Player 3",
      probWin: "55%",
      balance: 1200,
      bet: 60,
      cards: [
        { rank: "10", suit: "spades", faceUp: false }, // Face-down card
        { rank: "9", suit: "hearts", faceUp: true },
      ],
    },
  ]);

  const [communityCards, setCommunityCards] = useState([
    { rank: "10", suit: "spades", faceUp: false },
    { rank: "9", suit: "clubs", faceUp: true },
    { rank: "8", suit: "hearts", faceUp: true },
    { rank: "7", suit: "diamonds", faceUp: true },
    { rank: "6", suit: "spades", faceUp: true },
  ]);

  const pot = 500;
  const dealerIndex = 0;
  const pokerTableBackground = "PokerTable4.png";

  const playerPositions = getPlayerPositions(players.length);

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100vh",
        backgroundColor: "#2C5530",
        overflow: "hidden",
      }}
    >
      <img
        src={pokerTableBackground}
        alt="Poker Table"
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "100%",
          height: "auto",
        }}
      />

      <div
        style={{
          position: "absolute",
          top: "58%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          color: "white",
          fontWeight: "bold",
          fontSize: "20px",
        }}
      >
        Pot: ${pot}
      </div>

      {players.map((player, index) => {
        const { x, y } = playerPositions[index];
        return (
          <div
            key={index}
            style={{
              position: "absolute",
              left: x,
              top: y,
              color: "white",
              textAlign: "center",
              width: "150px",
              transform: "translate(-50%, -50%)",
            }}
          >
            <div
              style={{
                position: "absolute",
                left: "60%",
                top: "0%",
                transform: "translate(-50%, -50%)",
                display: "flex",
                zIndex: 1,
                marginTop: "-15px",
              }}
            >
              {player.cards.map((card, idx) => (
                <img
                  key={idx}
                  src={loadCardImage(card.rank, card.suit, card.faceUp)}
                  alt={`${card.rank} of ${card.suit}`}
                  style={{
                    width: "95px",
                    height: "auto",
                    transform: `rotate(${idx === 0 ? -5 : 5}deg)`,
                    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.3)",
                  }}
                />
              ))}
            </div>

            <div
              style={{
                position: "relative",
                zIndex: 2,
              }}
            >
              <div
                style={{
                  padding: "15px",
                  backgroundColor: "#1c2a1e",
                  borderRadius: "10px",
                  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
                  color: "white",
                  textAlign: "center",
                  width: "150px",
                  margin: "0 auto",
                  zIndex: 2,
                }}
              >
                <h3 style={{ margin: "5px 0", fontSize: "16px" }}>
                  {player.name}: {player.probWin}
                </h3>
                <p style={{ margin: "5px 0", fontSize: "14px" }}>
                  Bet: ${player.bet}
                </p>
                <p style={{ margin: "5px 0", fontSize: "14px" }}>
                  Balance: ${player.balance}
                </p>
              </div>
            </div>
          </div>
        );
      })}

      <div
        style={{
          position: "absolute",
          top: "45%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          gap: "15px",
        }}
      >
        {communityCards.map((card, index) => (
          <img
            key={index}
            src={loadCardImage(card.rank, card.suit, card.faceUp)}
            alt={`${card.rank} of ${card.suit}`}
            style={{
              width: "100px",
              height: "auto",
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default PokerGameUI;
