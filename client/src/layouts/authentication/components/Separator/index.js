/**/

// @mui material components
import Divider from "@mui/material/Divider";

// Vision UI Dashboard React components
import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";

function Separator() {
  return (
    <VuiBox position="relative" py={0.25}>
      <Divider />
      <VuiBox
        bgColor="white"
        position="absolute"
        top="50%"
        left="50%"
        px={1.5}
        lineHeight={1}
        sx={{ transform: "translate(-50%, -60%)" }}
      >
        <VuiTypography variant="button" fontWeight="medium" color="text">
          or
        </VuiTypography>
      </VuiBox>
    </VuiBox>
  );
}

export default Separator;
