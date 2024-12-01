// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Optional: Add your global styles here
import App from './App'; // Import the root component (App)

// Render the root component inside the div with the id 'root' (usually defined in index.html)
ReactDOM.render(
  <React.StrictMode>
    <App />  {/* This will render your Poker game */}
  </React.StrictMode>,
  document.getElementById('root') // The div in your public/index.html file
);

