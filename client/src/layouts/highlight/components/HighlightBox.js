import React, { useState } from "react";
import { Card, useMediaQuery } from "@mui/material";
import CheatsheetImage from "assets/images/highlights/cc14_1.png";


function HighlightBox() {
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Breakpoint für Responsive Design

  return (
    <div
      style={{
        width: "100%",
        height: isSmallScreen ? "300px" : "80vw",
        minHeight: "100vh", // Mindesthöhe für den kleinen Bildschirm
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "auto", // Scrollbar hinzufügen, falls Inhalt überläuft
        transition: "all 0.3s ease",
      }}
      >
      <Card
        sx={{
          width: "90%", // Set card width to 90%
          height: "90%", // Set card height to 90%
          backgroundColor: "rgba(255, 255, 255, 0.1)",
          borderRadius: "20px",
          display: "flex",
          flexDirection: "row", // Display elements next to each other
          justifyContent: "space-between",
          alignItems: "center",
          position: "relative",
          padding: "20px",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.3)",
          overflow: "hidden", // Avoid overflowing content
        }}
      >
        {/* Component Rendering */}
        <div
          style={{
            display: "flex",
            flexDirection: "column", // Stack iframe and image vertically
            justifyContent: "center", // Center content vertically in the inner container
            alignItems: "center", // Center content horizontally in the inner container
            width: "100%",
            justifyContent: "space-between", // Ensure space between iframe and image
            height: "100%", // Fill available height
          }}
        >
          <iframe
            src="https://www.spacex.com/vehicles/starship/"
            width="60%" // Set iframe width to 45%
            height="60%" // Set iframe height to 100% of parent height
            title="Starship Launch"
            allowFullScreen="true"
            style={{
              borderRadius: "15px", // Adding rounded corners to iframe
            }}
          />
          <div
          style={{
            display: "flex",
            justifyContent: "center", // Center content vertically in the inner container
            alignItems: "center", // Center content horizontally in the inner container
            width: "100%",
            justifyContent: "space-between", // Ensure space between iframe and image
            gap: "40px", // Add 10px gap between iframe and image
            height: "100%", // Fill available height
          }}
          >
            <img
                src={CheatsheetImage}
                alt="Campus Kneipe"
                style={{
                  //objectFit: "contain",
                  width: "47%", // Set image width to 45%
                  height: "62%", // Set image height to 100% of parent height
                  padding: "3px",
                  borderRadius: "16px",
                  filter: "contrast(1.3) brightness(0.9) hue-rotate(5deg) saturate(1)",
                }}
              />
              <iframe
                src="https://m4rkus28.codeberg.page/Mandelbrot-Generator-WebappST/@works/Fraktalgenerator.html"
                width="60%" // Set iframe width to 45%
                height="62%" // Set iframe height to 100% of parent height
                title="Mandelbrot"
                allowFullScreen="true"
                style={{
                  borderRadius: "15px", // Adding rounded corners to iframe
                }}
              />
            </div>


          </div>
          
      </Card>
    </div>
  );
}

export default HighlightBox;