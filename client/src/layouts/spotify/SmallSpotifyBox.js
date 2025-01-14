import React from "react";
import { Card } from "@mui/material";
import SpotifyComponent from "./components/SpotifyComponent"; // Import der Spotify-Komponente

function SmallSpotifyBox() {
  return (
    <div
      style={{
        width: "100%",
        height: "45vh",
        margin: 0,
        padding: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        boxSizing: "border-box",
      }}
    >
      <Card
        sx={{
          width: "100%", // Dynamische Breite wie bei WelcomeMark
          height: "100%",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderRadius: "12px", // Gleiche Rundung wie bei der WelcomeMark-Komponente
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          alignItems: "center",
          padding: "8px",
          boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            transform: "scale(0.5)",
            transformOrigin: "center",
          }}
        >
          <SpotifyComponent useLyrics={false} />
        </div>
      </Card>
    </div>
  );
}

export default SmallSpotifyBox;