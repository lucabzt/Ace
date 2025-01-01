import React from "react";
import { Card } from "@mui/material";
import SpotifyComponent from "./components/SpotifyComponent"; // Importiert Spotify-Komponente

function SmallSpotifyBox() {
  return (
    <div
      style={{
        width: "100%",
        height: "40vh",
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
          width: "auto",
          maxWidth: "100%",
          height: "100%",
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderRadius: "10px",
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          alignItems: "center",
          padding: "8px",
          boxShadow: "0 2px 8px rgba(0, 0, 0, 0.2)",
          overflow: "hidden",
        }}
      >
        {/* Skalierungsstile für Kinderkomponenten */}
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
          {/* Rendern der Spotify-Komponente */}
          <SpotifyComponent />
        </div>
      </Card>

      {/* Button-spezifische Stile */}
      <style>
        {`
          button {
            width: 24px !important; /* Kleinere Breite für die Buttons */
            height: 24px !important; /* Kleinere Höhe für die Buttons */
            font-size: 12px !important; /* Kleinere Schriftgröße */
            padding: 4px !important; /* Kleinere Innenabstände */
          }
        `}
      </style>
    </div>
  );
}

export default SmallSpotifyBox;
