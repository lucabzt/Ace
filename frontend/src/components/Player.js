import React from "react";
import Card from "./Card";

const Player = ({ player, position, isDealer }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: position.x,
        top: position.y,
        color: player.folded ? "red" : "white",
        textAlign: "center",
        width: "150px",
        transform: "translate(-50%, -50%)",
      }}
    >
      {/* Dealer Button */}
      {isDealer && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            right: "-30px",
            transform: "translate(50%, -50%)",
            width: "30px",
            height: "30px",
            backgroundColor: "#FFD700",
            color: "black",
            borderRadius: "50%",
            fontSize: "14px",
            fontWeight: "bold",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.3)",
            zIndex: 3,
          }}
        >
          D
        </div>
      )}
      <div
        style={{
          position: "absolute",
          left: "60%", // Position cards near the player's profile
          top: "0%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          zIndex: 1,
          marginTop: "-15px", // Move closer vertically
        }}
      >
        {player.cards.map((card, idx) => (
          <Card key={idx} card={{ ...card, idx }} playerFolded={player.folded} />
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
            color: player.folded ? "red" : "white",
            textAlign: "center",
            width: "150px",
            margin: "0 auto",
            zIndex: 2,
          }}
        >
          <h3 style={{ margin: "5px 0", fontSize: "18px" }}>
            {player.name}: {player.probWin}
          </h3>
          <p style={{ margin: "5px 0", fontSize: "16px" }}>
            Bet: ${player.bet}
          </p>
          <p style={{ margin: "5px 0", fontSize: "16px" }}>
            Balance: ${player.balance}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Player;
