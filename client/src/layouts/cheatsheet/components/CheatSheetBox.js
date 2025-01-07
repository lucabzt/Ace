import React, { useState } from "react";
import { Card, useMediaQuery } from "@mui/material";

import CheatsheetCard from "./CheatSheetCard";
import VuiButton from "../../../components/VuiButton"; // Importiere VuiButton

function CheatSheetBox() {
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
          : "50vw",
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
        <CheatsheetCard/>
      </Card>
    </div>
  );
}

export default CheatSheetBox;