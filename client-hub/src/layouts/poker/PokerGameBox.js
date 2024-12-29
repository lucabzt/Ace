import React, { useState } from "react";
import { Card, Button, useMediaQuery } from "@mui/material";
import PokerGameUI from "./components/PokerGameUI/PokerGameUI";

function PokerGameBox() {
  const [isFullscreen, setIsFullscreen] = useState(false); // State für den Vollbildmodus
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Breakpoint

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const fullscreenStyles = isFullscreen
    ? {
        position: "fixed", // Rendering wird auf Bildschirm zentriert
        top: 0,
        left: 0,
        width: "100vw", // Full width in viewport
        height: "100vh", // Full height in viewport
        backgroundColor: "rgba(0, 0, 0, 0.9)", // Dark background
        zIndex: 9999, // Ensure it's on the highest z-axis
        overflow: "hidden", // Prevent scrolling outside the fullscreen element
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }
    : {};

  return (
    <div
      style={{
        ...fullscreenStyles,
        width: isFullscreen ? "100vw" : "100%", // im Vollbild ganze Breite
        height: isFullscreen
          ? "100vh" /* Max Größe */
          : isSmallScreen
          ? "300px" /* für mobile Viewports */
          : "40vw", /* Standardgröße */
        transition: "all 0.3s ease", // Weiche Übergänge umschaltend
      }}
    >
      <Card
        sx={{
          width: isFullscreen ? "95%" : "100%", // Larger width in fullscreen
          height: isFullscreen ? "95%" : "100%", // Larger height in fullscreen
          backgroundColor: "rgba(255, 255, 255, 0.1)", // Transparent card for fullscreen effect
          borderRadius: "20px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          position: "relative",
          boxShadow: isFullscreen
            ? "0 8px 20px rgba(255, 255, 255, 0.4)"
            : "0 4px 12px rgba(0, 0, 0, 0.3)", // Schattierungen
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
            backgroundColor: isFullscreen ? "#ff5252" : "#00bcd4", // Exit/Enter Farbe
            color: "#fff",
            "&:hover": {
              backgroundColor: isFullscreen ? "#e53935" : "#008c9e", // Hover
            },
            borderRadius: "8px",
            boxShadow: "0 4px 14px rgba(0, 0, 0, 0.3)",
          }}
        >
          {isFullscreen ? "Exit Fullscreen" : "Play Fullscreen"}
        </Button>
        {/* Poker-UI Rendering */}
        <PokerGameUI isFullscreen={isFullscreen} />
      </Card>
    </div>
  );
}

export default PokerGameBox;