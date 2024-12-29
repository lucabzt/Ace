import React, { useState, useEffect, useCallback } from "react";
import PokerGameUI from "../PokerGameUI/PokerGameUI";
import SlidePanel from "../SlidePanel/SlidePanel";
import SpotifyLogin from "../SlidePanel/SpotifyLogin";

import SpotifyPlayer from "../SlidePanel/SpotifyPlayer";

import './Layout.css';

const Layout = () => {
  const [showRaiseSlider, setShowRaiseSlider] = useState(false);
  const [raiseAmount, setRaiseAmount] = useState(0);
  const [token, setToken] = useState(null);
  const [layoutWidth, setLayoutWidth] = useState(23); // Initial width percentage for layout-container
  const [isDragging, setIsDragging] = useState(false);

  const [refreshtoken, setrefreshtoken] = useState(null);
  const [expridedata, setexpridedata] = useState(null);

  async function sendAction (action) {
    const response = await fetch('http://127.0.0.1:5000/player-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    });
  }

  const handleRaiseClick = () => {
    setShowRaiseSlider((prev) => !prev);
    if (!showRaiseSlider){
      sendAction("raise " + raiseAmount)
    }
  };

  const handleCheckClick = () => {
    sendAction("check")
  }

  const handleFoldClick = () => {
    sendAction("fold")
  }

  const handleSliderChange = (event) => {
    setRaiseAmount(event.target.value);
  };

  const handleSliderChangeSpotify = (event) => {
    setLayoutWidth(event.target.value);
  };

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

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("spotifyAccessToken");
    setToken(null);


  };


  const handleMouseMove = useCallback((event) => {
      if (!isDragging) return;

      const newWidth = (event.clientX / window.innerWidth) * 100;

      if (newWidth >= 0 && newWidth <= 100) {
        setLayoutWidth(newWidth);
      }
    }, [isDragging]);


  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    } else {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    }

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  return (
    <div className="main-container">
      {/* Left Panel (Spotify) */}
      <div  className="left-panel"  style={{ width: `${layoutWidth}%` }} >
      {token ? (
          <SpotifyPlayer token={token} expiresAt={expridedata} refreshToken={refreshtoken}/>
        ) : (
          <SpotifyLogin onLoginSuccess={(newToken) => setToken(newToken)} />
        )}
      </div>
      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
    {/* Slicer */}
    <div
      className="slicer"
      onMouseDown={handleMouseDown}
      style={{ cursor: "ew-resize" }}
    ></div>

      {/* Right Panel (Poker UI) */}

      <div className="right-panel" style={{ width: `${100 - layoutWidth}%` }}>
        <div className="poker-ui-container">
          <PokerGameUI/>

          {/* Bottom Buttons */}
          <div className="action-buttons">
            <button className="action-button" onClick={handleRaiseClick}>Raise</button>
            <button className="action-button" onClick={handleCheckClick}>Check</button>
            <button className="action-button" onClick={handleFoldClick}>Fold</button>
          </div>

          {/* Raise Slider */}
          {showRaiseSlider && (
              <div className="raise-slider">
                <input
                    type="range"
                    min="0"
                    max="500"
                    step="10"
                    value={raiseAmount}
                    onChange={handleSliderChange}
                />
                <p>Raise Amount: ${raiseAmount}</p>
              </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Layout;
