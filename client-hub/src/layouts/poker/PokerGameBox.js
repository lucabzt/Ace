import React, { useState } from "react";
import { Card, Button, useMediaQuery } from "@mui/material";
import PokerGameUI from "./components/PokerGameUI/PokerGameUI";

function PokerGameBox() {
  const [isFullscreen, setIsFullscreen] = useState(false); // Fullscreen State
  const [showRaiseSlider, setShowRaiseSlider] = useState(false); // Raise Slider State
  const [raiseAmount, setRaiseAmount] = useState(10); // Raise Amount
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Breakpoint for responsive design

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

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

  // Fullscreen styles
  const fullscreenStyles = isFullscreen
    ? {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0, 0, 0, 0.9)",
        zIndex: 9999,
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }
    : {};

  return (
    <div
      style={{
        ...fullscreenStyles,
        width: isFullscreen ? "100vw" : "100%",
        height: isFullscreen
          ? "100vh"
          : isSmallScreen
          ? "300px"
          : "40vw",
        transition: "all 0.3s ease",
      }}
    >
      <Card
        sx={{
          width: isFullscreen ? "95%" : "100%",
          height: isFullscreen ? "95%" : "100%",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderRadius: "20px",
          display: "flex",
          flexDirection: "column", // Ensure layout stacking for PokerUI + Buttons
          justifyContent: "center",
          alignItems: "center",
          position: "relative",
          padding: "20px",
          boxShadow: isFullscreen
            ? "0 8px 20px rgba(255, 255, 255, 0.4)"
            : "0 4px 12px rgba(0, 0, 0, 0.3)",
        }}
      >
        {/* Button für Vollbild */}
        <Button
          onClick={toggleFullscreen}
          variant="contained"
          sx={{
            position: "absolute",
            top: "10px",
            right: "10px",
            padding: "10px 20px",
            fontSize: "13px",
            backgroundColor: isFullscreen ? "#ff5252" : "#00bcd4",
            color: "#fff",
            "&:hover": {
              backgroundColor: isFullscreen ? "#e53935" : "#008c9e",
            },
            borderRadius: "8px",
            boxShadow: "0 4px 14px rgba(0, 0, 0, 0.3)",
          }}
        >
          {isFullscreen ? "Exit Fullscreen" : "Play Fullscreen"}
        </Button>

        {/* Poker-UI Rendering */}
        <PokerGameUI isFullscreen={isFullscreen} />

        {/* Bottom Buttons */}
        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          {/* Raise Button */}
          <button
            style={{
              backgroundColor: "royalblue",
              color: "white",
              border: "none",
              borderRadius: "8px",
              padding: "10px 15px",
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
            }}
            onClick={handleCallClick}
          >
            Call
          </button>
        </div>

        {/* Raise Slider */}
        {showRaiseSlider && (
          <div
            style={{
              marginTop: "20px",
              backgroundColor: "#2a2a2a",
              padding: "20px",
              borderRadius: "10px",
              textAlign: "center",
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
              }}
            >
              OK
            </button>
          </div>
        )}
      </Card>
    </div>
  );
}

export default PokerGameBox;