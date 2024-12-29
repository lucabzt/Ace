import { Grid, Card } from "@mui/material";
import { useMediaQuery } from "@mui/material";

// Vision UI Dashboard components
import VuiBox from "../../components/VuiBox";
import VuiTypography from "../../components/VuiTypography";

import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";
import WelcomeMark from "./components/WelcomeMark";

// Import Poker Game
import Poker from "../poker/PokerGameBox"; // Der Pfad zu `Poker.js` hängt von Ihrer Datei-Struktur ab

function Dashboard() {
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Breakpoint for smaller screens (responsive)

  // Spotify Placeholder: Replace with actual Spotify integration if needed
  const SpotifyPlaceholder = () => (
    <Card
      sx={{
        width: "100%",
        height: "210px", // Original Spotify box height
        backgroundColor: "rgba(30, 215, 96, 0.1)", // Original Spotify box color
        borderRadius: "20px",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <VuiTypography variant="h4" color="white" textAlign="center">
        Spotify Placeholder
      </VuiTypography>
    </Card>
  );

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        overflow: isSmallScreen ? "auto" : "hidden", // Allow scrolling only if width < 960px
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Dashboard Layout */}
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox py={3} sx={{ flexGrow: 1 }}>
          <VuiBox mb={3}>
            <Grid container spacing={2}>
              {/* Left Section: Welcome and Spotify */}
              <Grid item xs={12} lg={4} xl={2}>
                <VuiBox mb={3}>
                  <WelcomeMark />
                </VuiBox>
                <SpotifyPlaceholder />
              </Grid>

              {/* Right Section: Poker Game */}
              <Grid item xs={12} lg={8} xl={10}>
                <VuiBox
                  position="relative"
                  sx={{
                    width: "100%",
                    minHeight: "200px",
                    height: "auto",
                    transition: "all 0.3s ease",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                >
                  {/* Poker Game Integration */}
                  <Poker /> {/* Fügt das Poker-Spiel hinzu */}
                </VuiBox>
              </Grid>
            </Grid>
          </VuiBox>
        </VuiBox>
        {/* Footer */}
        <VuiBox mt="auto">
          <Footer />
        </VuiBox>
      </DashboardLayout>
    </div>
  );
}

export default Dashboard;