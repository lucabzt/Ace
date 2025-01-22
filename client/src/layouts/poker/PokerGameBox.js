import React, { useState } from "react";
import { Card, useMediaQuery } from "@mui/material";
import PokerGameUI from "./components/PokerGameUI/PokerGameUI";
import GameButtons from "./components/buttons/GameButtons";
import VuiButton from "../../components/VuiButton";
import { FullscreenExitRounded, FullscreenRounded } from "@mui/icons-material";

function PokerGameBox() {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const isSmallScreen = useMediaQuery("(max-width: 960px)");

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const fullscreenStyles = isFullscreen
    ? {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        backgroundColor: "rgba(0, 0, 0, 0.9)",
        zIndex: 9998,
        overflow: "hidden",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none", // Prevent the fullscreen container from blocking clicks
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
          : "50vw",
        transition: "all 0.3s ease",
        pointerEvents: "auto", // Restore interactivity for children
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
          overflow: "hidden",
        }}
      >
        {/* Fullscreen Button */}
        <VuiButton
          onClick={toggleFullscreen}
          variant="text" // Use "text" variant to remove background
          color="info"
          style={{
            position: "absolute",
            top: "20px",
            right: "20px",
            fontSize: "2rem",
            padding: "0",
            zIndex: 9999, // Ensure button is on top
            backgroundColor: "transparent", // Remove background color
            boxShadow: "none", // Remove any shadow
            minWidth: "auto", // Remove minimum width
            "&:hover": {
            backgroundColor: "transparent", // Ensure no background on hover
            },
            pointerEvents: "auto", // Make button clickable
          }}
        >
          {isFullscreen ? (
            <FullscreenExitRounded style={{ transform: "scale(2.5)", color: "white" }} />
          ) : (
            <FullscreenRounded style={{ transform: "scale(2.5)", color: "white" }} />
          )}
        </VuiButton>

        {/* Poker-UI Rendering */}
        <PokerGameUI isFullscreen={isFullscreen} />

        {/* Game Buttons */}
        <GameButtons />
      </Card>
    </div>
  );
}

export default PokerGameBox;