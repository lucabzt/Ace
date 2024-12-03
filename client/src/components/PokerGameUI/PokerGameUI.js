import React, { useState, useEffect } from "react";
import Player from "../Player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";
import { players } from "../../data/playersData";

const PokerGameUI = () => {
  const pokerTableBackground = "images/poker_table/PokerTable100.png";
  const [playerPositions, setPlayerPositions] = useState(getPlayerPositions(players.length));
  const [pot, setPot] = useState(null);
  const [communityCards, setCommunityCards] = useState([]); // State for community cards
  const [dealerIndex, setDealerIndex] = useState(null); // State for dealer index

  // Polling logic for pot, community cards, and dealer
  const pollGameData = () => {
    // Fetch pot value
    fetch("http://127.0.0.1:5000/pot")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch pot value");
        }
        return res.json();
      })
      .then((data) => {
        if (data.pot !== pot) {
          setPot(data.pot); // Update pot only if it changes
          console.log("Pot value updated:", data.pot);
        }
      })
      .catch((error) => console.error("Error fetching pot value:", error));

    // Fetch community cards
    fetch("http://127.0.0.1:5000/community-cards")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch community cards");
        }
        return res.json();
      })
      .then((data) => {
        // Compare fetched cards with current state before updating
        if (JSON.stringify(data) !== JSON.stringify(communityCards)) {
          setCommunityCards(data);
          console.log("Community cards updated:", data);
        }
      })
      .catch((error) => console.error("Error fetching community cards:", error));

    // Fetch dealer index
    fetch("http://127.0.0.1:5000/dealer")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch dealer index");
        }
        return res.json();
      })
      .then((data) => {
        if (data.dealerIndex !== dealerIndex) {
          setDealerIndex(data.dealerIndex); // Update dealer index only if it changes
          console.log("Dealer index updated:", data.dealerIndex);
        }
      })
      .catch((error) => console.error("Error fetching dealer index:", error));
  };

  // Poll data on component mount and at regular intervals
  useEffect(() => {
    pollGameData(); // Initial fetch
    const interval = setInterval(pollGameData, 3000); // Poll every 3 seconds
    return () => clearInterval(interval); // Cleanup on unmount
  }, [pot, communityCards, dealerIndex]); // Dependencies ensure changes are reflected dynamically

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
        const isDealer = index === dealerIndex; // Mark the current dealer
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
