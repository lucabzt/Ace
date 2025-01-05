export const getPlayerPositions = (numPlayers, boxWidth, boxHeight) => {
  const radiusX = boxWidth / 2.4; // Dynamischer Radius basierend auf der Box-Breite
  const radiusY = boxHeight / 2.9; // Dynamischer Radius basierend auf der Box-Höhe

  // Dynamische Anpassung von centerX basierend auf der Breite der Box:
  const baseOffset = boxWidth / 6; // Grundoffset abhängig von der Box-Breite
  const variableOffset = Math.min((boxWidth - 1800) / 3, 200); // Variabler Teil des Offsets
  const centerXOffset = Math.max(baseOffset + variableOffset, boxWidth / 10); // Minimaler Offset (z.B. 10% der Breite)

  const centerX = boxWidth / 2 - 50; // Horizontal zentriert mit dynamischem Offset
  const centerY = boxHeight / 2 + 40; // Vertikal bleibt konstant

  return Array.from({ length: numPlayers }, (_, i) => {
    const angle = (2 * Math.PI * i) / numPlayers; // Spieler gleichmäßig im Kreis verteilen
    return {
      x: centerX + radiusX * Math.cos(angle), // Horizontale Position berechnen
      y: centerY + radiusY * Math.sin(angle), // Vertikale Position berechnen
    };
  });
};