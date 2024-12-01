import React from "react";
import { loadCardImage } from "../utils/cardUtils";

const Card = ({ card, playerFolded }) => (
  <img
    src={loadCardImage(card.rank, card.suit, card.faceUp)}
    alt={`${card.rank} of ${card.suit}`}
    style={{
      width: "7vw",
      height: "auto",
      transform: `rotate(${card.idx === 0 ? -5 : 5}deg)`,
      boxShadow: "0 2px 4px rgba(0, 0, 0, 0.3)",
      filter: playerFolded ? "grayscale(100%)" : "none",
      marginLeft: card.idx !== 0 ? "-2vw" : "0", // Adjust negative margin for overlap
    }}
  />
);

export default Card;
