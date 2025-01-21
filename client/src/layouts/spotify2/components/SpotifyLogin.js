import React from "react";
import { useSpotify } from "./SpotifyContext";
import VuiButton from "../../../components/VuiButton";
import { FaSpotify } from "react-icons/fa";

const serverAddress = process.env.REACT_APP_SERVER_ADDRESS || "https://localhost:5000";

const SpotifyLogin = () => {
  const { setToken, setRefreshToken, setExpiresAt } = useSpotify();

  const handleLogin = () => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);

    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");
    const expiresAt = parseInt(params.get("expires_at"), 10);

    if (accessToken && refreshToken && expiresAt) {
      setToken(accessToken);
      setRefreshToken(refreshToken);
      setExpiresAt(Date.now() + expiresAt * 1000);

      sessionStorage.setItem("spotifyAccessToken", accessToken);
      window.location.hash = ""; // Clear the hash
    } else {
      console.error("Failed to extract tokens from URL hash.");
      window.location.href = `${serverAddress}/login`;
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
      <VuiButton
        onClick={handleLogin}
        className="spotify-button"
        variant="contained"
        color="info"
        style={{
          fontSize: "1.3rem",
          padding: "0.5rem 0.8rem",
          backgroundColor: "#1DB954",
          color: "black",
          borderRadius: "15px",
        }}
        aria-label="Login with Spotify"
      >
        <FaSpotify size={25} /> Login with Spotify
      </VuiButton>
    </div>
  );
};

export default SpotifyLogin;
