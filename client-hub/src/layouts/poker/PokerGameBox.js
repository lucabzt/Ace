import React, { useState } from "react";
import { Card, Button, useMediaQuery } from "@mui/material";
import PokerGameUI from "./components/PokerGameUI/PokerGameUI";
import GameButtons from "./components/buttons/GameButtons";

function PokerGameBox() {
  const [isFullscreen, setIsFullscreen] = useState(false); // Fullscreen State
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Breakpoint for responsive design

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
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
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          position: "relative",
          padding: "20px",
          boxShadow: isFullscreen
            ? "0 8px 20px rgba(255, 255, 255, 0.4)"
            : "0 4px 12px rgba(0, 0, 0, 0.3)",
        }}
      >
        {/* Fullscreen Button */}
        <Button
          onClick={toggleFullscreen}
          variant="contained"
          sx={{
            position: "absolute",
            top: "10px",
            right: "10px",
            padding: "10px 20px",
            fontSize: "13px",
            backgroundColor: isFullscreen ? "#ff5252" : "royalblue",
            color: "#fff",
            "&:hover": {
              backgroundColor: isFullscreen ? "#e53935" : "royalblue",
            },
            borderRadius: "8px",
            boxShadow: "0 4px 14px rgba(0, 0, 0, 0.3)",
          }}
        >
          {isFullscreen ? "Exit Fullscreen" : "Play Fullscreen"}
        </Button>

        {/* Poker-UI Rendering */}
        <PokerGameUI isFullscreen={isFullscreen} />

        {/* Game Buttons */}
        <GameButtons />
      </Card>
    </div>
  );
}

export default PokerGameBox;