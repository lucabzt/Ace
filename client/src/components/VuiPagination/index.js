/**/

import { forwardRef, createContext, useContext } from "react";

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

// Vision UI Dashboard React components
import VuiBox from "../VuiBox";

// Custom styles for VuiPagination
import VuiPaginationItemRoot from "./VuiPaginationItemRoot";

// The Pagination main context
const Context = createContext();

const VuiPagination = forwardRef(
  ({ item, variant, color, size, active, children, ...rest }, ref) => {
    const context = item ? useContext(Context) : null;
    const paginationSize = context ? context.size : null;

    return (
      <Context.Provider value={{ variant, color, size }}>
        {item ? (
          <VuiPaginationItemRoot
            {...rest}
            ref={ref}
            variant={active ? context.variant : "outlined"}
            color={active ? context.color : "text"}
            iconOnly
            circular
            ownerState={{ variant, active, paginationSize }}
          >
            {children}
          </VuiPaginationItemRoot>
        ) : (
          <VuiBox
            display="flex"
            justifyContent="flex-end"
            alignItems="center"
            sx={{ listStyle: "none" }}
          >
            {children}
          </VuiBox>
        )}
      </Context.Provider>
    );
  }
);

// Setting default values for the props of VuiPagination
VuiPagination.defaultProps = {
  item: false,
  variant: "gradient",
  color: "info",
  size: "medium",
  active: false,
};

// Typechecking props for the VuiPagination
VuiPagination.propTypes = {
  item: PropTypes.bool,
  variant: PropTypes.oneOf(["gradient", "contained"]),
  color: PropTypes.oneOf([
    "white",
    "primary",
    "secondary",
    "info",
    "success",
    "warning",
    "error",
    "light",
    "dark",
  ]),
  size: PropTypes.oneOf(["small", "medium", "large"]),
  active: PropTypes.bool,
  children: PropTypes.node.isRequired,
};

export default VuiPagination;
