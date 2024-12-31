import React from "react";

const DealerButton = () => (
  <div
    style={{
      position: "absolute",
      top: "50%",
      right: "-30px",
      transform: "translate(50%, -50%)",
      width: "30px",
      height: "30px",
      backgroundColor: "#FFD700",
      color: "black",
      borderRadius: "50%",
      fontSize: "14px",
      fontWeight: "bold",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      boxShadow: "0 2px 4px rgba(0, 0, 0, 0.3)",
      zIndex: 3,
    }}
  >
    D
  </div>
);

export default DealerButton;
