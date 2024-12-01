// src/components/Pot.js
import React from 'react';

const Pot = ({ pot }) => {
  return (
    <div style={{ position: 'absolute', top: '50%', left: '50%' }}>
      <h2>Pot: {pot}</h2>
    </div>
  );
};

export default Pot;
