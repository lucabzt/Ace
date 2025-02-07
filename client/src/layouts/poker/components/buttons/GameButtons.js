import React, { useState } from "react";
// Import VuiButton für einheitliches Styling
import VuiButton from "../../../../components/VuiButton";

//const serverAddress = process.env.PUBLIC_URL;
const serverAddress = "https://localhost:5000";
console.log("Server Address:", serverAddress);

function GameButtons() {
  const [showRaiseSlider, setShowRaiseSlider] = useState(false); // Raise Slider State
  const [raiseAmount, setRaiseAmount] = useState(10); // Raise Amount

  // Fetch player data
  const fetchPlayers = () => {
    fetch(`${serverAddress}/players`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch players data");
        }
        return res.json();
      })
  };

  // API-Anfrage, um Spieleraktionen zu senden
  const sendAction = async (action) => {
    await fetch(`${serverAddress}/player-action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: action }),
    });
  };

  // Button-Click-Handler
  const handleRaiseClick = () => {
    setShowRaiseSlider((prev) => !prev);
  };

  const handleConfirmRaise = () => {
    sendAction("raise " + raiseAmount);
    setShowRaiseSlider(false); // Slider verstecken
  };

  const handleCheckClick = () => {
    sendAction("check");
  };

  const handleFoldClick = () => {
    sendAction("fold");
  };

  const handleCallClick = () => {
    sendAction("call");
  };

  // Slider-Änderungen verarbeiten
  const handleSliderChange = (event) => {
    setRaiseAmount(event.target.value);
  };

  return (
    <div style={{ position: "relative" }}>
      {/* Raise-Area wird bedingt gerendert */}
      {showRaiseSlider && (
        <div
          style={{
            position: "absolute",
            bottom: "100%",
            left: "50%",
            transform: "translateX(-50%)",
            width: "100%",
            maxWidth: "300px", // Reduzierte Breite
            padding: "10px", // Reduziertes Padding
            backgroundColor: "#1c2a1e",
            borderRadius: "0.5rem", // Abgerundete Ecken
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)", // Leichter Schatten
            textAlign: "center",
            zIndex: 1000,
          }}
        >
          <input
            type="range"
            min="10"
            max="1000"
            step="10"
            value={raiseAmount}
            onChange={handleSliderChange}
            style={{
              width: "100%",
              margin: "0.2rem 0", // Weniger Abstand
            }}
          />
          <p style={{ color: "#fff", margin: "0.2rem 0", fontSize: "1rem" }}>
            Raise Amount: ${raiseAmount}
          </p>
          <VuiButton
            onClick={handleConfirmRaise}
            variant="contained"
            color="info"
            style={{
              marginTop: "0.4rem",
              fontSize: "0.88rem", // Schriftgröße angepasst
              padding: "0.44rem 0.88rem", // Padding-Anpassung für Skalierung
            }}
          >
            OK
          </VuiButton>
        </div>
      )}

      {/* Bedienelemente-Buttons unten */}
      <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
        <VuiButton
          variant="contained"
          color="info"
          onClick={handleRaiseClick}
          style={{
            fontSize: "1.2rem", // Schriftgröße erhöht
            padding: "0.55rem 1.2rem", // Padding um 10 % erhöht
          }}
        >
          Raise
        </VuiButton>
        <VuiButton
          variant="contained"
          color="info"
          onClick={handleCallClick}
          style={{
            fontSize: "1.2rem",
            padding: "0.55rem 1.2rem",
          }}
        >
          Call
        </VuiButton>
        <VuiButton
          variant="contained"
          color="info"
          onClick={handleCheckClick}
          style={{
            fontSize: "1.2rem",
            padding: "0.55rem 1.2rem",
          }}
        >
          Check
        </VuiButton>
        <VuiButton
          variant="contained"
          color="info"
          onClick={handleFoldClick}
          style={{
            fontSize: "1.2rem",
            padding: "0.55rem 1.2rem",
          }}
        >
          Fold
        </VuiButton>
      </div>
    </div>
  );
}

export default GameButtons;