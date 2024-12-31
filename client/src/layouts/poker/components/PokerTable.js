import React from "react";
import "./PokerTable.css";

const PokerTable = ({ pokerTableBackground, pot, children, isFullscreen }) => (
  <div
    className="table"
    style={{
      position: "relative",
      margin: "auto", // Zentriert den Container horizontal und vertikal
      width: isFullscreen ? "100%" : "90%", // Vollbild im Fokus
      maxWidth: isFullscreen ? "none" : "1200px", // keine Einschränkung
      height: isFullscreen ? "100vh" : "70vh", // Bildschirmhöhe
      overflow: "auto",
      display: "table",
      justifyContent: "center",
      alignItems: "center",
      border: isFullscreen ? "5px solid #ffcc00" : "2px solid transparent", // Breitere Grenzen
      transition: "all 0.3s ease",
    }}
  >
    <img
      src={pokerTableBackground}
      alt="Poker Table"
      style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: isFullscreen ? "130%" : "100%", // Bildanpassung
        height: isFullscreen ? "110%" : "100%",
        objectFit: "cover",
      }}
    />
    <div
      style={{
        position: "absolute",
        bottom: isFullscreen ? "40%" : "23%", // Fokus neu platzieren
        left: "50%",
        transform: "translate(-50%, -50%)",
        color: "white",
        fontWeight: "bold",
        fontSize: isFullscreen ? "2vw" : "1.5vw", // Fokus dynamisch
        textAlign: "center",
      }}
    >
      Pot: ${pot}
    </div>
    {children}
  </div>
);

export default PokerTable;