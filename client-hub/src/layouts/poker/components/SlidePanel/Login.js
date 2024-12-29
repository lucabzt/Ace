import React, { useEffect, useState } from "react";

const Login = () => {
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    // Parse access token from URL hash
    const hash = window.location.hash;
    const token = hash
      .substring(1)
      .split("&")
      .find((item) => item.startsWith("access_token"))
      ?.split("=")[1];

    if (token) {
      setAccessToken(token);
      localStorage.setItem("spotifyAccessToken", token);
    }
  }, []);

  const loginWithSpotify = () => {
    window.location.href = "http://localhost:8888/login"; // Redirect to backend login
  };

  return (
    <div>
      {accessToken ? (
        <p>Logged in with token: {accessToken}</p>
      ) : (
        <button onClick={loginWithSpotify}>Login with Spotify</button>
      )}
    </div>
  );
};

export default Login;
