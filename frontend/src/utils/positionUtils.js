export const getPlayerPositions = (numPlayers) => {
  const radiusX = window.innerWidth / 2.5;
  const radiusY = window.innerHeight / 2.7;
  const centerX = window.innerWidth / 2 - 20;
  const centerY = window.innerHeight / 2 + 40;

  return Array.from({ length: numPlayers }, (_, i) => {
    const angle = (2 * Math.PI * i) / numPlayers;
    return {
      x: centerX + radiusX * Math.cos(angle),
      y: centerY + radiusY * Math.sin(angle),
    };
  });
};
