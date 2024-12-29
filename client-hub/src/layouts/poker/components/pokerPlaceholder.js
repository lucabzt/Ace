import React from "react";
import { Card } from "@mui/material";
import VuiBox from "../../../components/VuiBox";
import VuiTypography from "../../../components/VuiTypography";

import gif from "../../../assets/images/cardimgfree.png"; // Beispielhintergrund-Bild

function PokerEmbed() {
  return (
    <VuiBox
      display="flex"
      justifyContent="center"
      alignItems="center"
      sx={{
        width: "100%", // Behält die ursprüngliche Breite bei
        height: "600px", // Feste Höhe wie im Original
        backgroundImage: `url(${gif})`, // Hintergrundbild
        backgroundSize: "cover", // Vollständig abdeckendes Hintergrundbild
        backgroundPosition: "center", // Zentriert
        borderRadius: "20px", // Abgerundete Ecken wie WelcomeMark
      }}
    >
      <Card
        sx={{
          width: "100%",
          height: "100%",
          backgroundColor: "transparent", // Der Hintergrund bleibt durchsichtig, um keinen grauen Hintergrund zu bekommen
          boxShadow: "none", // Entfernt Schatten um das Card-Element, falls nötig
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <VuiTypography variant="h4" color="white" textAlign="center">
          Poker Embed Placeholder
        </VuiTypography>
      </Card>
    </VuiBox>
  );
}

export default PokerEmbed;