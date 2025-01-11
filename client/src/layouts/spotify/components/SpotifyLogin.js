import React from "react";
import VuiButton from "../../../components/VuiButton";
import { FaSpotify } from "react-icons/fa"; // Import des Spotify-Icons

const serverAddress = "https://localhost:5000"; // Backend-Adresse
console.log("Server Address:", serverAddress);

const SpotifyLogin = ({ onLoginSuccess }) => {
  const loginWithSpotify = () => {
    // Umleitung zur Spotify-Authentifizierungs-URL des Servers
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
    color: "black",
    border: "none",
    cursor: "pointer",
    borderRadius: "15px",
    display: "flex",
    alignItems: "center",
    gap: "0.5rem",
  };

  return (
    <div style={centerStyle}>
      <VuiButton
        onClick={loginWithSpotify}
        className="spotify-button"
        variant="contained"
        color="info"
        style={buttonStyle}
      >
        <FaSpotify size={25} /> {/* Spotify-Icon */}
        Login with Spotify
      </VuiButton>
    </div>
  );
};

export default SpotifyLogin;