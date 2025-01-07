import Card from "@mui/material/Card";
import CheatsheetImage from "assets/images/cheatsheet/hand_ranking.JPG";
import PropTypes from "prop-types";

import VuiBox from "../../../components/VuiBox";
import VuiTypography from "../../../components/VuiTypography";

// React Icons (removed as no additional icons are needed)

import billingCard from "assets/images/curved-images/white-curved.jpeg";

function CheatsheetCard({ userName }) {
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
        {/* Benutzername */}
        <VuiTypography
          variant="h4"
          fontWeight="bold"
          color="black"
          mb={2}
        >
          {userName}
        </VuiTypography>

        {/* Cheatsheet Image */}
        <VuiBox
          component="img"
          src={CheatsheetImage}
          alt="Cheatsheet: Hand Ranking"
          width="100%"
          height="auto"
        />
      </VuiBox>
    </Card>
  );
}

CheatsheetCard.defaultProps = {
  userName: "Hand Ranking",
};

CheatsheetCard.propTypes = {
  userName: PropTypes.string,
};

export default CheatsheetCard;