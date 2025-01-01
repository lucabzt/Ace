import React from "react";

import { Card, Icon } from "@mui/material";
import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";

import gif from "../../../../assets/images/cardimgfree.png";

const WelcomeMark = () => {
  return (
    <Card sx={() => ({
      height: "100%",
      py: "20px",
      backgroundImage: `url(${gif})`,
      backgroundSize: "cover",
      backgroundPosition: "50%"
    })}>
      <VuiBox height="100%" display="flex" flexDirection="column" justifyContent="space-between">
        <VuiBox>
          {/* Schriftgröße ist angepasst */}
          <VuiTypography
            color="text"
            variant="button"
            fontWeight="regular"
            mb="8px"
            sx={{ fontSize: "14px" }} // Schriftgröße erhöht
          >
            Welcome back,
          </VuiTypography>
          <VuiTypography
            color="white"
            variant="h5"
            fontWeight="bold"
            mb="12px"
            sx={{ fontSize: "20px" }} // Schriftgröße erhöht
          >
            Sebastian
          </VuiTypography>
          <VuiTypography
            color="text"
            variant="body2"
            fontWeight="regular"
            mb="auto"
            sx={{ fontSize: "14px" }} // Schriftgröße erhöht
          >
            Glad to see you again!
            <br /> Ask me anything.
          </VuiTypography>
        </VuiBox>
        <VuiTypography
          component="a"
          href="#"
          variant="button"
          color="white"
          fontWeight="regular"
          sx={{
            fontSize: "14px", // Größere Schriftgröße
            mr: "5px",
            display: "inline-flex",
            alignItems: "center",
            cursor: "pointer",

            "& .material-icons-round": {
              fontSize: "1.2rem", // Icon angepasst
              transform: `translate(2px, -0.5px)`,
              transition: "transform 0.2s cubic-bezier(0.34,1.61,0.7,1.3)",
            },

            "&:hover .material-icons-round, &:focus  .material-icons-round": {
              transform: `translate(6px, -0.5px)`,
            },
          }}
        >
          Tap to record
          <Icon sx={{ fontWeight: "bold", ml: "5px", fontSize: "1.2rem" }}>arrow_forward</Icon>
        </VuiTypography>
      </VuiBox>
    </Card>
  );
};

export default WelcomeMark;