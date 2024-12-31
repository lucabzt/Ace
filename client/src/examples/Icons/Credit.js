/**/

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

// Vision UI Dashboard React base styles
import colors from "../../assets/theme/base/colors";

function Credit({ color, size }) {
  return (
    <svg width="23" height="23" width={size} height={size} xmlns="http://www.w3.org/2000/svg">
      <path
        fill={colors[color] ? colors[color].main : colors.dark.main}
        d="M1.406 17.023a2.461 2.461 0 002.461 2.46h14.766a2.461 2.461 0 002.46-2.46v-6.768H1.407v6.768zm2.9-3.34a1.318 1.318 0 011.319-1.318h2.11a1.318 1.318 0 011.318 1.318v.879a1.318 1.318 0 01-1.319 1.318H5.625a1.318 1.318 0 01-1.318-1.318v-.879zM18.633 4.014H3.867a2.46 2.46 0 00-2.46 2.461v1.143h19.687V6.475a2.46 2.46 0 00-2.461-2.46z"
      />
    </svg>
  );
}

// Setting default values for the props of Credit
Credit.defaultProps = {
  color: "dark",
  size: "16px",
};

// Typechecking props for the Credit
Credit.propTypes = {
  color: PropTypes.oneOf([
    "primary",
    "secondary",
    "info",
    "success",
    "warning",
    "error",
    "dark",
    "light",
    "white",
  ]),
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default Credit;
