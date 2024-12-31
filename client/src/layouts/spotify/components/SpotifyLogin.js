import React from "react";


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

  return (
    <div style={centerStyle}>
      <button onClick={loginWithSpotify} className="spotify-button">
        Login with Spotify
      </button>
    </div>
  );
};

export default SpotifyLogin;
