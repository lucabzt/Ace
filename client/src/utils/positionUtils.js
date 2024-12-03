export const getPlayerPositions = (numPlayers) => {
  const tableWidth = window.innerWidth * 0.8; // Adjust table size based on window width
  const tableHeight = window.innerHeight * 0.6; // Adjust table height based on window height
  const radiusX = tableWidth / 2.5; // Adjust the X radius based on table width
  const radiusY = tableHeight / 1.8; // Adjust the Y radius based on table height

  const centerX = window.innerWidth / 2.55; // Center X position in the viewport
  const centerY = window.innerHeight * 0.5; // Center Y position (slightly above the bottom)

  return Array.from({ length: numPlayers }, (_, i) => {
    const angle = (2 * Math.PI * i) / numPlayers; // Distribute players evenly around the circle
    return {
      x: centerX + radiusX * Math.cos(angle), // X position around the circle
      y: centerY + radiusY * Math.sin(angle), // Y position around the circle
    };
  });
};
