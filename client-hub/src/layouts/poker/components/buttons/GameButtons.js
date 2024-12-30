import React, { useState } from "react";

function GameButtons() {
  const [showRaiseSlider, setShowRaiseSlider] = useState(false); // Raise Slider State
  const [raiseAmount, setRaiseAmount] = useState(10); // Raise Amount

  // API request to send player action
  const sendAction = async (action) => {
    await fetch("http://127.0.0.1:5000/player-action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: action }),
    });
  };

  // Button click handlers
  const handleRaiseClick = () => {
    setShowRaiseSlider((prev) => !prev);
  };

  const handleConfirmRaise = () => {
    sendAction("raise " + raiseAmount);
    setShowRaiseSlider(false); // Hide the slider after confirming
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

  // Slider change handler
  const handleSliderChange = (event) => {
    setRaiseAmount(event.target.value);
  };

  return (
    <div>
      {/* Conditionally Render Raise Area */}
      {showRaiseSlider && (
        <div
          style={{
            position: "absolute",
            bottom: "100px", // Adjust this value as needed to position it above the buttons
            width: "80%",
            maxWidth: "400px",
            backgroundColor: "rgba(42, 42, 42, 0.95)",
            padding: "20px",
            borderRadius: "10px",
            textAlign: "center",
            zIndex: 1000, // Ensure it's above other elements
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
              margin: "10px 0",
            }}
          />
          <p style={{ color: "#fff" }}>Raise Amount: ${raiseAmount}</p>
          <button
            onClick={handleConfirmRaise}
            style={{
              backgroundColor: "royalblue",
              color: "white",
              border: "none",
              borderRadius: "8px",
              padding: "10px 15px",
              marginTop: "10px",
              cursor: "pointer",
            }}
          >
            OK
          </button>
        </div>
      )}

      {/* Bottom Buttons */}
      <div style={{ display: "flex", gap: "20px", marginTop: "20px", position: "relative" }}>
        {/* Raise Button */}
        <button
          style={{
            backgroundColor: "royalblue",
            color: "white",
            border: "none",
            borderRadius: "10px",
            padding: "10px 15px",
            cursor: "pointer",
          }}
          onClick={handleRaiseClick}
        >
          Raise
        </button>

        {/* Check Button */}
        <button
          style={{
            backgroundColor: "royalblue",
            color: "white",
            border: "none",
            borderRadius: "8px",
            padding: "10px 15px",
            cursor: "pointer",
          }}
          onClick={handleCheckClick}
        >
          Check
        </button>

        {/* Fold Button */}
        <button
          style={{
            backgroundColor: "royalblue",
            color: "white",
            border: "none",
            borderRadius: "8px",
            padding: "10px 15px",
            cursor: "pointer",
          }}
          onClick={handleFoldClick}
        >
          Fold
        </button>

        {/* Call Button */}
        <button
          style={{
            backgroundColor: "royalblue",
            color: "white",
            border: "none",
            borderRadius: "8px",
            padding: "10px 15px",
            cursor: "pointer",
          }}
          onClick={handleCallClick}
        >
          Call
        </button>
      </div>
    </div>
  );
}

export default GameButtons;