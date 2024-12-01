import React from "react";

const PokerTable = ({ pokerTableBackground, pot, children }) => (
  <div
    style={{
      position: "relative",
      width: "100%",
      height: "100vh",
      backgroundColor: "#2C5530",
      overflow: "hidden",
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
        width: "100%",
        height: "auto",
      }}
    />
    <div
      style={{
        position: "absolute",
        top: "58%", // Adjust the positioning for the pot text
        left: "50%",
        transform: "translateX(-50%)",
        color: "white",
        fontWeight: "bold",
        fontSize: "2vw",  // Responsive font size based on viewport width
      }}
    >
      {/* Pot Text */}
      Pot: ${pot}
    </div>
    {children}
  </div>
);

export default PokerTable;
