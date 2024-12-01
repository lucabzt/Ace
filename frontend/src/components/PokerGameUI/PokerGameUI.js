import React, { useState, useEffect } from "react";
import Player from "../Player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";
import { players } from "../../data/playersData";

const PokerGameUI = () => {
  const dealerIndex = 2;
  const pokerTableBackground = "PokerTable100.png";
  const [playerPositions, setPlayerPositions] = useState(getPlayerPositions(players.length));
  const [pot, setPot] = useState(null);
  const [communityCards, setCommunityCards] = useState([]); // State for community cards

  // Fetch pot value
  const fetchPot = () => {
    fetch("http://127.0.0.1:5000/pot") // Directly call Flask API
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch pot value");
        }
        return res.json();
      })
      .then((data) => {
        setPot(data.pot);
        console.log("Pot value updated:", data.pot);
      })
      .catch((error) => {
        console.error("Error fetching pot value:", error);
      });
  };

  // Fetch community cards
  const fetchCommunityCards = () => {
    fetch("http://127.0.0.1:5000/community-cards") // Call Flask API for community cards
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch community cards");
        }
        return res.json();
      })
      .then((data) => {
        setCommunityCards(data); // Update state with fetched community cards
        console.log("Community cards updated:", data);
      })
      .catch((error) => {
        console.error("Error fetching community cards:", error);
      });
  };

  // Fetch pot and community cards on component mount
  useEffect(() => {
    fetchPot(); // Fetch pot
    fetchCommunityCards(); // Fetch community cards

    const interval = setInterval(fetchPot, 3000); // Poll pot every 3 seconds
    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  // Handle window resize for player positions
  useEffect(() => {
    const handleResize = () => {
      setPlayerPositions(getPlayerPositions(players.length));
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [players.length]);

  return (
    <PokerTable pokerTableBackground={pokerTableBackground} pot={pot !== null ? pot : "Loading..."}>
      {players.map((player, index) => {
        const position = playerPositions[index];
        const isDealer = index === dealerIndex;
        return (
          <Player key={index} player={player} position={position} isDealer={isDealer} />
        );
      })}

      {/* Render community cards dynamically */}
      <div
        style={{
          position: "absolute",
          top: "45%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          display: "flex",
          gap: "1vw",
        }}
      >
        {communityCards.map((card, index) => (
          <img
            key={index}
            src={loadCardImage(card.rank, card.suit, card.faceUp)}
            alt={`${card.rank} of ${card.suit}`}
            style={{ width: "6vw", height: "auto" }}
          />
        ))}
      </div>
    </PokerTable>
  );
};

export default PokerGameUI;
