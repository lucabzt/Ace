import React from "react";
import ReactDOM from 'react-dom';
import { BrowserRouter } from "react-router-dom";
import App from "./App";

// Vision UI Dashboard React Context Provider
import { VisionUIControllerProvider } from "./context";

import { SpotifyProvider } from "./layouts/spotify2/components/SpotifyContext";


ReactDOM.render(
  <SpotifyProvider>
    <BrowserRouter>
      <VisionUIControllerProvider>
        <App />
      </VisionUIControllerProvider>
    </BrowserRouter>
  </SpotifyProvider>
,
  document.getElementById('root')
);