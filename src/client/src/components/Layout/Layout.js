import React, { useState } from "react";
import PokerGameUI from "../PokerGameUI/PokerGameUI";
import SlidePanel from "../SlidePanel/SlidePanel";
import './Layout.css';

const Layout = () => {
  const [showRaiseSlider, setShowRaiseSlider] = useState(false);
  const [raiseAmount, setRaiseAmount] = useState(0);

  const handleRaiseClick = () => {
    setShowRaiseSlider((prev) => !prev);
  };

  const handleSliderChange = (event) => {
    setRaiseAmount(event.target.value);
  };

  return (
    <div className="layout-container">
      {/* Left Panel (Slide) */}
      <SlidePanel />

      {/* Right Side (Poker UI) */}
      <div className="poker-ui-container">
        <PokerGameUI />

        {/* Bottom Buttons */}
        <div className="action-buttons">
          <button className="action-button" onClick={handleRaiseClick}>Raise</button>
          <button className="action-button">Check</button>
          <button className="action-button">Fold</button>
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
  );
};

export default Layout;
