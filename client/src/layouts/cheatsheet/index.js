import React, { useEffect } from "react";
import Grid from "@mui/material/Grid";
import VuiBox from "../../components/VuiBox";

import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";
import CheatSheet from "./components/CheatSheetCard";
import ChipDistributionCard from "./components/ChipDistributionCard";
import Chart from "./components/PokerHeatMap";
import PokerGameBox from "../poker/PokerGameBox";
import PokerHeatmap from "./components/PokerHeatMap";
import background from "../../assets/images/body-background.png";

function Billing() {

  return (
    <div
      style={{
        width: "100vw",
        minHeight: "100vh",
        overflow: "auto",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <DashboardLayout>
        <DashboardNavbar />
        <VuiBox mt={4}>

          <VuiBox mb={1.5}>
            {/* Heatmap container */}
          <PokerHeatmap />
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <CheatSheet />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <ChipDistributionCard />
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </VuiBox>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    </div>
  );
}

export default Billing;
