import React from "react";
import { useMediaQuery } from "@mui/material";

// Vision UI Dashboard components
import VuiBox from "../../components/VuiBox";
import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";

// Import SpotifyBox
import SpotifyBox from "./SpotifyBox";

function Spotify() {
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Responsive Breakpoint

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        overflow: isSmallScreen ? "auto" : "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox
          py={3}
          display="flex"
          justifyContent="center"
          alignItems="center"
          sx={{ width: "100%" }}
        >
          {/* Render SpotifyBox */}
          <SpotifyBox />
        </VuiBox>
        <VuiBox mt="auto">
          <Footer />
        </VuiBox>
      </DashboardLayout>
    </div>
  );
}

export default Spotify;