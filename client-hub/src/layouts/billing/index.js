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
import PaymentMethod from "./components/PaymentMethod";
import Invoices from "./components/Invoices";
import BillingInformation from "./components/BillingInformation";
import Transactions from "./components/Transactions";
import CreditBalance from "./components/CreditBalance";

function Billing() {
  return (
    <DashboardLayout>
      <DashboardNavbar />
      <VuiBox mt={4}>
        <VuiBox mb={1.5}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={7} xl={8}>
              <Grid container spacing={3}>
                <Grid item xs={12} xl={6}>
                  <MasterCard number={7812213908237916} valid="05/24" cvv="09X" />
                </Grid>
                <Grid item xs={12} md={12} xl={6}>
                  <CreditBalance />
                </Grid>
                <Grid item xs={12}>
                  <PaymentMethod />
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={12} lg={5} xl={4}>
              <Invoices />
            </Grid>
          </Grid>
        </VuiBox>
        <VuiBox my={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={7}>
              <BillingInformation />
            </Grid>
            <Grid item xs={12} md={5}>
              <Transactions />
            </Grid>
          </Grid>
        </VuiBox>
      </VuiBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Billing;
