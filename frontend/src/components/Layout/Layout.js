// src/components/Layout/Layout.js
import React from "react";
import PokerGameUI from "../PokerGameUI/PokerGameUI";
import SlidePanel from "../SlidePanel/SlidePanel";
import './Layout.css';

const Layout = () => {
  return (
    <div className="layout-container">
      {/* Left Panel (Slide) */}
      <SlidePanel />

      {/* Right Side (Poker UI) */}
      <div className="poker-ui-container">
        <PokerGameUI />

        {/* Additional Panel Below Poker UI */}
        <div className="bottom-panel">
          <h3>Additional Information</h3>
          <p>Here you can add more details like player stats, etc.</p>
        </div>
      </div>
    </div>
  );
};

export default Layout;
