import Card from "@mui/material/Card";
import QRCodeImage from "assets/images/PayPal-QR-Code.png";
import PropTypes from "prop-types";

import VuiBox from "../../../../components/VuiBox";
import VuiTypography from "../../../../components/VuiTypography";

// React Icons für das PayPal-Logo
import { FaCcPaypal } from "react-icons/fa6"; // Alternatives Icon von react-icons

import billingCard from "assets/images/curved-images/white-curved.jpeg";

function PayPalCard({ userName }) {
  return (
    <Card
  sx={{
    background: `url('${billingCard}') no-repeat center center, linear-gradient(135deg, #0070ba, #1546a0)`,
    backgroundSize: "cover",
    backdropFilter: "blur(31px)",
    borderRadius: "16px",
    color: "black",
  }}
>
      <VuiBox p={2} pt={0} textAlign="center" position="relative">
        {/* PayPal-Logo als Icon */}
        <VuiBox
          display="flex"
          justifyContent="center"
          alignItems="center"
          sx={{
            position: "absolute",
            top: "16px",
            left: "16px",
            backgroundColor: "white",
            borderRadius: "50%",
            padding: "8px",
            boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.2)",
          }}
        >
          <FaCcPaypal size={32} color="#003087" /> {/* Alternatives Logo */}
        </VuiBox>

        {/* Benutzername */}
        <VuiTypography
          variant="h4"
          fontWeight="bold"
          color="black"
          mb={2}
        >
          {userName}
        </VuiTypography>

        {/* QR Code */}
        <VuiBox
          component="img"
          src={QRCodeImage}
          alt="QR Code"
          width="150px"
          height="150px"
          mx="auto"
        />

        {/* Scan-Anleitung */}
        <VuiTypography
          variant="subtitle1"
          fontWeight="medium"
          color="black"
          mt={2}
        >
          Scan this to pay
        </VuiTypography>
      </VuiBox>
    </Card>
  );
}

PayPalCard.defaultProps = {
  userName: "Sebastian Rogg",
};

PayPalCard.propTypes = {
  userName: PropTypes.string,
};

export default PayPalCard;