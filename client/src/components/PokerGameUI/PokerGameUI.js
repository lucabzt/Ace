import React, { useState, useEffect } from "react";
import Player from "../Player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";


const PROTOCOL="http";
const HOST_URL="127.0.0.1";
const HOST_PORT="5000";
const URI=`${PROTOCOL}://${HOST_URL}:${HOST_PORT}`


const PokerGameUI = () => {
  const pokerTableBackground = "images/poker_table/PokerTable100.png";
  const [players, setPlayers] = useState([]); // State for players
  const [playerPositions, setPlayerPositions] = useState([]);
  const [pot, setPot] = useState(null);
  const [communityCards, setCommunityCards] = useState([]);
  const [dealerIndex, setDealerIndex] = useState(null);

  // Fetch player data
  const fetchPlayers = () => {
    fetch(`${URI}/players`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch players data");
        }
        return res.json();
      })
      .then((data) => {
        setPlayers(data);
        setPlayerPositions(getPlayerPositions(data.length)); // Update positions
        console.log("Players data updated:", data);
      })
      .catch((error) => console.error("Error fetching players data:", error));
  };

  // Polling logic for other game data
  const pollGameData = () => {
    fetch(`${URI}/pot`)
      .then((res) => res.json())
      .then((data) => setPot(data.pot))
      .catch((error) => console.error("Error fetching pot value:", error));

    fetch(`${URI}/community-cards`)
      .then((res) => res.json())
      .then((data) => setCommunityCards(data))
      .catch((error) => console.error("Error fetching community cards:", error));

    fetch(`${URI}/dealer`)
      .then((res) => res.json())
      .then((data) => setDealerIndex(data.dealerIndex))
      .catch((error) => console.error("Error fetching dealer index:", error));
  };

  useEffect(() => {
    fetchPlayers(); // Fetch players initially
    pollGameData(); // Fetch other game data initially
    const interval = setInterval(() => {
      fetchPlayers(); // Update players
      pollGameData(); // Update other game data
    }, 500);
    return () => clearInterval(interval); // Cleanup on unmount
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
        return <Player key={index} player={player} position={position} isDealer={isDealer} />;
      })}

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
