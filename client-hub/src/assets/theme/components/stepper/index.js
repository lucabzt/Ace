/**/

// Vision UI Dashboard React base styles
import colors from "../../base/colors";

// Vision UI Dashboard React helper functions
import pxToRem from "../../functions/pxToRem";

const { transparent } = colors;

export default {
  styleOverrides: {
    root: {
      margin: `${pxToRem(48)} 0`,
      padding: `0 ${pxToRem(12)}`,

      "&.MuiPaper-root": {
        backgroundColor: transparent.main,
      },
    },
  },
};
