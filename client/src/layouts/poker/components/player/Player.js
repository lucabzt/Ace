import React from "react";
import Card from "../Card";

const Player = ({ player, position, isDealer }) => {
  const scale = 0.8; // zentrale Konstante, die die Größe in Prozent steuert (0 = 0%, 1 = 100%)

  return (
    <div
      style={{
        position: "absolute",
        left: position.x,
        top: position.y,
        color: player.folded ? "red" : "white",
        textAlign: "center",
        width: `${15 * scale}vw`, // Breitere Spielerprofil-Box, skaliert
        transform: "translate(-50%, -50%)",
      }}
    >
      {/* Dealer Button */}
      {isDealer && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            right: `${2 * scale}vw`, // Position des Dealer-Buttons, skaliert
            transform: "translate(50%, -50%)",
            width: `${2.5 * scale}vw`, // Skalierte Größe
            height: `${2.5 * scale}vw`,
            backgroundColor: "#FFD700",
            color: "black",
            borderRadius: "50%",
            fontSize: `${1.2 * scale}vw`, // Skalierte Schriftgröße
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
          left: "50%", // Karten zentrieren
          top: "0%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          zIndex: 1,
          marginTop: `${0.5 * scale}vw`, // Skalierter Abstand
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
            padding: `${0.2 * scale}vw`, // Skalierter Innenabstand
            backgroundColor: "rgba(28, 42, 30, 0.97)", // Hinzufügen von 20% Transparenz
            borderRadius: `${1.5 * scale}vw`, // Skalierte Rundung
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)", // Stärkere Schatten
            color: player.folded ? "red" : "white",
            textAlign: "center",
            width: `${10 * scale}vw`, // Skalierte Box-Breite
            margin: "0 auto",
            zIndex: 2,
          }}
        >
          <h3 style={{ margin: `${0.4 * scale}vw 0`, fontSize: `${1 * scale}vw` }}> {/* Skalierte Schriftgröße */}
            {player.name}: {player.probWin}%
          </h3>
          <p style={{ margin: `${0.4 * scale}vw 0`, fontSize: `${0.8 * scale}vw` }}> {/* Skalierte Schriftgröße */}
            Bet: ${player.bet}
          </p>
          <p style={{ margin: `${0.4 * scale}vw 0`, fontSize: `${0.8 * scale}vw` }}> {/* Skalierte Schriftgröße */}
            Balance: ${player.balance}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Player;