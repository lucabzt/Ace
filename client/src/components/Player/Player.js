import React from "react";
import Card from "../Card";

const Player = ({ player, position, isDealer }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: position.x,
        top: position.y,
        color: player.folded ? "red" : "white",
        textAlign: "center",
        width: "15vw",  // Reduced width for the player profile
        transform: "translate(-50%, -50%)",
      }}
    >
      {/* Dealer Button */}
      {isDealer && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            right: "2vw", // Adjust position
            transform: "translate(50%, -50%)",
            width: "2.5vw",  // Scaled dealer button size
            height: "2.5vw",
            backgroundColor: "#FFD700",
            color: "black",
            borderRadius: "50%",
            fontSize: "1.2vw", // Scaled font size for "D"
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

      {/* Player Cards */}
      <div
        style={{
          position: "absolute",
          left: "50%", // Keep the cards centered for better positioning
          top: "0%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          zIndex: 1,
          marginTop: "-1vw", // Adjust margin for responsive layout
        }}
      >
        {player.cards.map((card, idx) => (
          <Card key={idx} card={{ ...card, idx }} playerFolded={player.folded} />
        ))}
      </div>

      {/* Player Information */}
      <div
        style={{
          position: "relative",
          zIndex: 2,
        }}
      >
        <div
          style={{
            padding: "0.4vw",  // Reduced padding for more proportional layout
            backgroundColor: "#1c2a1e",
            borderRadius: "1vw",  // Scaled border radius
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
            color: player.folded ? "red" : "white",
            textAlign: "center",
            width: "10vw",  // Reduced width to make the text box smaller
            margin: "0 auto",
            zIndex: 2,
          }}
        >
          <h3 style={{ margin: "0.4vw 0", fontSize: "1vw" }}> {/* Reduced font size */}
            {player.name}: {player.probWin}
          </h3>
          <p style={{ margin: "0.4vw 0", fontSize: "0.9vw" }}> {/* Reduced font size */}
            Bet: ${player.bet}
          </p>
          <p style={{ margin: "0.4vw 0", fontSize: "0.9vw" }}> {/* Reduced font size */}
            Balance: ${player.balance}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Player;
