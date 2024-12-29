
// @mui material components
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Icon from "@mui/material/Icon";
import Link from "@mui/material/Link";

// Vision UI Dashboard React components
import VuiButton from "../../components/VuiButton";
import VuiBox from "../../components/VuiBox";
import VuiTypography from "../../components/VuiTypography";

// Custom styles for the SidenavCard
import { card, cardContent, cardIconBox, cardIcon } from "./styles/sidenavCard";

// Vision UI Dashboard React context
import { useVisionUIController } from "../../context";

function SidenavCard({ color, ...rest }) {
  const [controller] = useVisionUIController();
  const { miniSidenav, sidenavColor } = controller;

  return (
    <Card sx={(theme) => card(theme, { miniSidenav })}>
    </Card>
  );
}

export default SidenavCard;
