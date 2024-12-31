/**/

// @mui material components
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid";
import Icon from "@mui/material/Icon";
import Tooltip from "@mui/material/Tooltip";

// Vision UI Dashboard React components
import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";
import VuiButton from "../../../../components/VuiButton";

// Vision UI Dashboard React base styles
import borders from "../../../../assets/theme/base/borders";

// Images
import colors from "../../../../assets/theme/base/colors";

// Vision UI Dashboard component exemples
import Mastercard from "../../../../examples/Icons/Mastercard";
import Visa from "../../../../examples/Icons/Visa";

function PaymentMethod() {
  const { grey } = colors;

  return (
    <Card id="delete-account">
      <VuiBox display="flex" justifyContent="space-between" alignItems="center" mb="32px">
        <VuiTypography variant="lg" fontWeight="bold" color="white">
          Payment Method
        </VuiTypography>
        <VuiButton variant="contained" color="info">
          ADD NEW CARD
        </VuiButton>
      </VuiBox>
      <VuiBox>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <VuiBox
              border="2px solid"
              borderRadius="20px"
              borderColor={grey[600]}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              p="22px 20px"
            >
              <Mastercard width="21px" />
              <VuiTypography pl={2} variant="button" color="white" fontWeight="medium">
                7812 2139 0823 XXXX
              </VuiTypography>
              <VuiBox ml="auto" lineHeight={0}>
                <Tooltip title="Edit Card" placement="top">
                  <Icon sx={{ cursor: "pointer", color: "#fff" }} fontSize="small">
                    edit
                  </Icon>
                </Tooltip>
              </VuiBox>
            </VuiBox>
          </Grid>
          <Grid item xs={12} md={6}>
            <VuiBox
              border="2px solid"
              borderRadius="20px"
              borderColor={grey[600]}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              p="22px 20px"
            >
              <Visa width="25px" />
              <VuiTypography pl={2} variant="button" color="white" fontWeight="medium">
                7812 2139 0823 XXXX
              </VuiTypography>
              <VuiBox ml="auto" lineHeight={0}>
                <Tooltip title="Edit Card" placement="top">
                  <Icon sx={{ cursor: "pointer", color: "#fff" }} fontSize="small">
                    edit
                  </Icon>
                </Tooltip>
              </VuiBox>
            </VuiBox>
          </Grid>
        </Grid>
      </VuiBox>
    </Card>
  );
}

export default PaymentMethod;
