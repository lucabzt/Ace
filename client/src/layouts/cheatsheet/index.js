import React from "react";
import { useMediaQuery } from "@mui/material";

// Vision UI Dashboard components
import VuiBox from "../../components/VuiBox";
import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";

// Import PokerGameBox
import CheatsheetPlaceHolder from "../poker/utils/pokerPlaceholder";
import CheatSheetBox from "./components/CheatSheetBox";

function CheatSheet() {
  const isSmallScreen = useMediaQuery("(max-width: 960px)"); // Responsive breakpoint for smaller screens

  return (
      <div
          style={{
              width: "100vw", // Take full width
              height: "100vh", // Full height for the entire page
              overflow: "auto", // Immer das Scrollen erlauben
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
                  <CheatSheetBox/>
              </VuiBox>
              {/* Footer */}
              <VuiBox mt="auto">
                  <Footer/>
              </VuiBox>
          </DashboardLayout>
      </div>
  );
}

export default CheatSheet;