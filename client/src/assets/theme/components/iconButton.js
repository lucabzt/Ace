
// Vision UI Dashboard React Base Styles
import colors from "../base/colors";

const { transparent } = colors;

export default {
  styleOverrides: {
    root: {
      "&:hover": {
        backgroundColor: transparent.main,
      },
    },
  },
};
