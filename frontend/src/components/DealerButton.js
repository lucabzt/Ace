// src/components/DealerButton.js
import React from 'react';

const DealerButton = ({ x, y }) => {
  const dealerButtonImage = require('../assets/images/DealerButton.png');
  return (
    <div style={{ position: 'absolute', left: x, top: y }}>
      <img src={dealerButtonImage} alt="Dealer Button" width={40} height={40} />
    </div>
  );
};

export default DealerButton;
