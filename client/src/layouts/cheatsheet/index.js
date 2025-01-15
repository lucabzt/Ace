import React, { useEffect } from "react";
import Grid from "@mui/material/Grid";
import VuiBox from "../../components/VuiBox";

import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";
import CheatSheet from "./components/CheatSheetCard";
import ChipDistributionCard from "./components/ChipDistributionCard";
import Chart from "./components/Heatmap.json";

function Billing() {
  useEffect(() => {
    // Load AnyChart dynamically
    const script = document.createElement("script");
    script.src = "https://cdn.anychart.com/releases/8.11.0/js/anychart-bundle.min.js";
    script.async = true;
    script.onload = () => {
      // Verify if Chart contains the JSON configuration
      if (typeof Chart === "object" && Chart.chart) {
        const heatmap = window.anychart.fromJson(Chart); // Convert JSON to AnyChart instance
        heatmap.container("heatmap-container");
        heatmap.draw();
      } else {
        console.error("Chart is not a valid AnyChart configuration JSON.");
      }
    };
    document.body.appendChild(script);

    return () => {
      // Cleanup script when component unmounts
      document.body.removeChild(script);
    };
  }, []);

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
          {/* Heatmap container */}
          <div id="heatmap-container" style={{ width: "100%", height: "500px" }}></div>
        </VuiBox>
        <Footer />
      </DashboardLayout>
    </div>
  );
}

export default Billing;
