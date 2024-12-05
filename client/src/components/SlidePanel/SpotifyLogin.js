import React from "react";

const SpotifyLogin = ({ onLoginSuccess }) => {
  const loginWithSpotify = () => {
    // Redirect to your Flask server's Spotify authorization endpoint
    window.location.href = "http://127.0.0.1:5000/login";
  };

  const centerStyle = {
    display: "grid",
    justifyContent: "center",
    alignItems: "center",
    height: "200px",
  };

  return (
    <div style={centerStyle}>
      <button onClick={loginWithSpotify} className="spotify-button">
        Login with Spotify
      </button>
    </div>
  );
};

export default SpotifyLogin;
