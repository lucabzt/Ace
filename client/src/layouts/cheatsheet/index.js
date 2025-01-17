import React, { useEffect } from "react";
import Grid from "@mui/material/Grid";
import VuiBox from "../../components/VuiBox";

import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";
import ChipDistributionCard from "./components/ChipDistributionCard";
import PokerHeatmap from "./components/PokerHeatMap";

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
            <ChipDistributionCard />
          </VuiBox>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    </div>
  );
}

export default Billing;
