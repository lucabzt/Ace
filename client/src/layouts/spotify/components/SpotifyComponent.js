
import React, { useEffect, useState, useRef } from "react";

import SpotifyLogin from "./SpotifyLogin";
import SpotifyPlayer from "./SpotifyPlayer";

const SpotifyComponent = () => {

    const [token, setToken] = useState(null);
    const [refreshtoken, setrefreshtoken] = useState(null);
    const [expridedata, setexpridedata] = useState(null);

    
    useEffect(() => {
        // Extract access token from the URL hash
        const hash = window.location.hash;
        const refresh_token = hash
          .substring(1)
          .split("&")
          .find((param) => param.startsWith("refresh_token"))
          ?.split("=")[1];
          setrefreshtoken(refresh_token);
    
          const accessToken = hash
          .substring(1)
          .split("&")
          .find((param) => param.startsWith("access_token"))
          ?.split("=")[1];
    
          const expires_at = hash
          .substring(1)
          .split("&")
          .find((param) => param.startsWith("expires_at"))
          ?.split("=")[1];
          setexpridedata(expires_at);
    
        if (accessToken) {
          console.log("Access Token Found:", accessToken);
          setToken(accessToken); // Update state with token
          localStorage.setItem("spotifyAccessToken", accessToken); // Save token to localStorage
          window.location.hash = ""; // Clear URL hash
        } else {
          // Check if token is already stored in localStorage
          const storedToken = localStorage.getItem("spotifyAccessToken");
          if (storedToken) {
            console.log("Using Stored Token:", storedToken);
            setToken(storedToken);
          }
        }
      }, []);
    
      return (
        <div>
            {token ? (
                <SpotifyPlayer token={token} expiresAt={expridedata} refreshToken={refreshtoken}/>
            ) : (
                <SpotifyLogin onLoginSuccess={(newToken) => setToken(newToken)} />
            )}
        </div>);
}




export default SpotifyComponent;