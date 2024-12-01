export const getPlayerPositions = (numPlayers) => {
  const radiusX = window.innerWidth / 2.4;
  const radiusY = window.innerHeight / (2.7 + (numPlayers > 6 ? 0.2 : 0)); // Slightly smaller radius for more players
  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight * 0.55;

  return Array.from({ length: numPlayers }, (_, i) => {
    const angle = (2 * Math.PI * i) / numPlayers;
    return {
      x: centerX + radiusX * Math.cos(angle),
      y: centerY + radiusY * Math.sin(angle),
    };
  });
};
