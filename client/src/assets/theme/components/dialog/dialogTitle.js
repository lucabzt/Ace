/**/

// Vision UI Dashboard React base styles
import typography from "../../base/typography";

// Vision UI Dashboard React helper functions
import pxToRem from "../../functions/pxToRem";

const { size } = typography;

export default {
  styleOverrides: {
    root: {
      padding: pxToRem(16),
      fontSize: size.xl,
    },
  },
};
