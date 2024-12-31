/**/

// prop-types is a library for typechecking of props
import PropTypes from "prop-types";

function Mastercard({ width, height }) {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 21 15"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="6.63158" cy="7.49999" r="6.63158" fill="#EB001B" />
      <circle cx="14.3685" cy="7.49999" r="6.63158" fill="#F79E1B" />
    </svg>
  );
}

// Setting default values for the props of Mastercard
Mastercard.defaultProps = {
  color: "dark",
  size: "16px",
};

// Typechecking props for the Mastercard
Mastercard.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default Mastercard;
