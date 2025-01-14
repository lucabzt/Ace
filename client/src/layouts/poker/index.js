import React from "react";
import { useMediaQuery } from "@mui/material";

// Vision UI Dashboard components
import VuiBox from "../../components/VuiBox";
import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";

// Import PokerGameBox
import PokerGameBox from "./PokerGameBox";

function Poker() {
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Responsive breakpoint for smaller screens

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
              <DashboardNavbar/>
              <VuiBox
                  py={3}
                  display="flex"
                  justifyContent="center"
                  alignItems="center"
                  sx={{width: "100%"}}
              >
                  {/* Render PokerGameBox */}
                  <PokerGameBox/>
              </VuiBox>
              {/* Footer */}
              <VuiBox mt="auto">
                  <Footer/>
              </VuiBox>
          </DashboardLayout>
      </div>
  );
}

export default Poker;