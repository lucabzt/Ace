
// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

function SpadeLogo({ size }) {
  return (
    <svg
      version="1.0"
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 96.000000 96.000000"
      preserveAspectRatio="xMidYMid meet"
    >
      <g
        transform="translate(0.000000,96.000000) scale(0.100000,-0.100000)"
        fill="white"
        stroke="none"
      >
        <path
          d="M348 699 c-140 -141 -170 -183 -182 -255 -28 -168 160 -272 263 -146 l31 37 0 -28 c0 -37 -21 -85 -54 -124 -24 -28 -25 -32 -9 -36 31 -9 182 -7 188 2 3 5 -6 23 -20 39 -31 37 -55 93 -55 128 0 26 1 26 30 -14 88 -121 270 -47 270 110 0 80 -39 139 -188 288 l-137 136 -137 -137z"
        />
      </g>
    </svg>
  );
}

// Setting default values for the props of SimmmpleLogo
SpadeLogo.defaultProps = {
  color: "dark",
  size: "16px",
};

// Typechecking props for the SimmmpleLogo
SpadeLogo.propTypes = {
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

export default SpadeLogo;
