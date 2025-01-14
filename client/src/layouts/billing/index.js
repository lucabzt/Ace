/**/

// @mui material components
import Grid from "@mui/material/Grid";

// Vision UI Dashboard React components
import VuiBox from "../../components/VuiBox";

// Vision UI Dashboard React components
import MasterCard from "../../examples/Cards/MasterCard";
// Vision UI Dashboard React example components
import DashboardLayout from "../../examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "../../examples/Navbars/DashboardNavbar";
import Footer from "../../examples/Footer";

// Billing page components
import Transactions from "./components/Transactions";
import PayPalCard from "./components/PayPal/PayPalCard";

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
          <DashboardNavbar/>
          <VuiBox mt={4}>
            <VuiBox mb={1.5}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <PayPalCard userName={"Sebastian Rogg"} qrCode="assets/images/paypal-qr-code.png"/>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Transactions/>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </VuiBox>
          </VuiBox>
          <Footer/>
        </DashboardLayout>
        </div>
        );
        }

        export default Billing;
