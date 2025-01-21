import React, { createContext, useContext, useState, useEffect } from "react";

const SpotifyContext = createContext();

export const useSpotify = () => useContext(SpotifyContext);

export const SpotifyProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [expiresAt, setExpiresAt] = useState(null);

  const baseURL = process.env.REACT_APP_SERVER_ADDRESS || "https://localhost:5000";

  useEffect(() => {
    const refreshAccessToken = async () => {
      try {
        if (!refreshToken || !expiresAt) {
          console.error("Missing refresh token or expiration time.");
          return;
        }

        const response = await fetch(`${baseURL}/refresh_token?refresh_token=${refreshToken}`);
        if (response.ok) {
          const data = await response.json();
          const newToken = data.access_token;
          const newExpiresIn = data.expires_in;

          setToken(newToken);
          setExpiresAt(Date.now() + newExpiresIn * 1000);
          sessionStorage.setItem("spotifyAccessToken", newToken);
        } else {
          console.error("Failed to refresh token:", response.statusText);
        }
      } catch (err) {
        console.error("Error refreshing token:", err);
      }
    };

    if (refreshToken && expiresAt) {
      const timeUntilExpiry = expiresAt - Date.now() - 60000; // Refresh 1 minute before expiration
      if (timeUntilExpiry > 0) {
        const timeout = setTimeout(refreshAccessToken, timeUntilExpiry);
        return () => clearTimeout(timeout);
      } else {
        refreshAccessToken();
      }
    }
  }, [refreshToken, expiresAt, baseURL]);

  return (
    <SpotifyContext.Provider
      value={{ token, setToken, refreshToken, setRefreshToken, expiresAt }}
    >
      {children}
    </SpotifyContext.Provider>
  );
};
