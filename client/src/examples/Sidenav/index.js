import React, { useEffect, useState } from "react";
import { useLocation, NavLink } from "react-router-dom";
import PropTypes from "prop-types";

// @mui material components
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import Icon from "@mui/material/Icon";

// Vision UI Dashboard React components
import VuiBox from "../../components/VuiBox";
import VuiTypography from "../../components/VuiTypography";
import VuiButton from "../../components/VuiButton";

// Vision UI Dashboard React example components
import SidenavCollapse from "./SidenavCollapse";
import SidenavRoot from "./SidenavRoot";
import sidenavLogoLabel from "./styles/sidenav";

// Vision UI Dashboard React context
import { useVisionUIController, setMiniSidenav, setTransparentSidenav } from "../../context";

// Vision UI Dashboard React icons
import SpadeLogo from "../Icons/SpadeLogo";

function Sidenav({ color, brandName, routes, ...rest }) {
  const [controller, dispatch] = useVisionUIController();
  const { miniSidenav, transparentSidenav } = controller;
  const location = useLocation();
  const { pathname } = location;
  const collapseName = pathname.split("/").slice(1)[0];
  const [isFullscreen, setIsFullscreen] = useState(false);

  const closeSidenav = () => setMiniSidenav(dispatch, true);

  const toggleSidenav = () => {
    setMiniSidenav(dispatch, !miniSidenav);
  };

  // Listen for fullscreen change
  useEffect(() => {
    function checkFullscreen() {
      setIsFullscreen(
        document.fullscreenElement !== null ||
          document.webkitFullscreenElement !== null ||
          document.mozFullScreenElement !== null ||
          document.msFullscreenElement !== null
      );
    }

    document.addEventListener("fullscreenchange", checkFullscreen);
    document.addEventListener("webkitfullscreenchange", checkFullscreen);
    document.addEventListener("mozfullscreenchange", checkFullscreen);
    document.addEventListener("MSFullscreenChange", checkFullscreen);

    return () => {
      document.removeEventListener("fullscreenchange", checkFullscreen);
      document.removeEventListener("webkitfullscreenchange", checkFullscreen);
      document.removeEventListener("mozfullscreenchange", checkFullscreen);
      document.removeEventListener("MSFullscreenChange", checkFullscreen);
    };
  }, []);

  // Handle sidenav resizing dynamically
  useEffect(() => {
    function handleMiniSidenav() {
      setMiniSidenav(dispatch, window.innerWidth < 1200);
    }

    window.addEventListener("resize", handleMiniSidenav);
    handleMiniSidenav();

    return () => window.removeEventListener("resize", handleMiniSidenav);
  }, [dispatch]);

  useEffect(() => {
    if (window.innerWidth < 1440) {
      setTransparentSidenav(dispatch, false);
    }
  }, []);

  const renderRoutes = routes.map(({ type, name, icon, title, noCollapse, key, route, href }) => {
    let returnValue;

    if (type === "collapse") {
      returnValue = href ? (
        <a href={href} key={key} target="_blank" rel="noreferrer" style={{ textDecoration: "none" }}>
          <SidenavCollapse
            color={color}
            name={name}
            icon={icon}
            active={key === collapseName}
            noCollapse={noCollapse}
          />
        </a>
      ) : (
        <NavLink to={route} key={key}>
          <SidenavCollapse
            color={color}
            key={key}
            name={name}
            icon={icon}
            active={key === collapseName}
            noCollapse={noCollapse}
          />
        </NavLink>
      );
    } else if (type === "title") {
      returnValue = (
        <VuiTypography
          key={key}
          color="white"
          display="block"
          variant="caption"
          fontWeight="bold"
          textTransform="uppercase"
          pl={3}
          mt={2}
          mb={1}
          ml={1}
        >
          {title}
        </VuiTypography>
      );
    } else if (type === "divider") {
      returnValue = <Divider light key={key} />;
    }

    return returnValue;
  });

  return (
    <>
      {/* Sidebar */}
      <SidenavRoot {...rest} variant="permanent" ownerState={{ transparentSidenav, miniSidenav }}>
        <VuiBox pt={2} px={4} textAlign="center" sx={{ overflow: "unset !important" }}>
          <VuiBox
            display={{ xs: "block", xl: "none" }}
            position="absolute"
            top={0}
            right={0}
            p={1.5}
            onClick={closeSidenav}
            sx={{ cursor: "pointer" }}
          >
            <VuiTypography variant="h6" color="text">
              <Icon sx={{ fontWeight: "bold" }}>close</Icon>
            </VuiTypography>
          </VuiBox>
          <VuiBox
            component={NavLink}
            to="/"
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            <VuiBox
              display="flex"
              alignItems="center"
              justifyContent="center"
              sx={theme => sidenavLogoLabel(theme, { miniSidenav })}
            >
              <SpadeLogo size="24px" style={{ marginRight: "8px" }} />
              <VuiTypography
                variant="button"
                textGradient={true}
                color="logo"
                fontWeight="medium"
                sx={{
                  opacity: miniSidenav ? 0 : 1,
                  maxWidth: miniSidenav ? 0 : "100%",
                  whiteSpace: "nowrap",
                }}
              >
                {brandName}
              </VuiTypography>
            </VuiBox>
          </VuiBox>
        </VuiBox>
        <Divider light />
        <List>{renderRoutes}</List>
      </SidenavRoot>

      {/* Toggle Button for Fullscreen */}
      <div
        style={{
          position: "fixed",
          top: "20px",
          left: miniSidenav ? "96px" : "250px",
          transition: "left 300ms ease-in-out",
          zIndex: 1000,
        }}
      >
        <VuiButton variant="contained" color="secondary" onClick={toggleSidenav}>
          <Icon>{miniSidenav ? "menu_open" : "menu"}</Icon>
        </VuiButton>
      </div>
    </>
  );
}

Sidenav.defaultProps = {
  color: "info",
};

Sidenav.propTypes = {
  color: PropTypes.oneOf(["primary", "secondary", "info", "success", "warning", "error", "dark"]),
  brandName: PropTypes.string.isRequired,
  routes: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default Sidenav;