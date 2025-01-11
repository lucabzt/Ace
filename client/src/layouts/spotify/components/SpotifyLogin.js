import React from "react";
import VuiButton from "../../../components/VuiButton";


const serverAddress = "https://localhost:5000";//process.env.BACKEND_URL;
console.log("Server Address:", serverAddress);

const SpotifyLogin = ({ onLoginSuccess }) => {
  const loginWithSpotify = () => {
    // Redirect to your Flask server's Spotify authorization endpoint
    window.location.href = `${serverAddress}/login`;
  };

  const centerStyle = {
    display: "grid",
    justifyContent: "center",
    alignItems: "center",
    height: "200px",
  };

  const buttonStyle = {
    fontSize: "1.3rem",
    padding: "0.5rem 0.8rem",
    backgroundColor: "#1DB954",
    border: "none",
    cursor: "pointer",
    borderRadius: "15px",
  };
  return (
    <div style={centerStyle}>
      <VuiButton
          onClick={loginWithSpotify}
          className="spotify-button"
          variant="contained"
          color="info" style={buttonStyle}>
        Login with Spotify
      </VuiButton>
    </div>
  );
};

export default SpotifyLogin;
