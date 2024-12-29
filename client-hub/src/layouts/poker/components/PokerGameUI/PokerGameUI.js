import React, { useState, useEffect, useRef } from "react";
import Player from "../Player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";
import PokerTableBackground from "../images/poker_table/PokerTable100.png";

const PROTOCOL = "http";
const HOST_URL = "127.0.0.1";
const HOST_PORT = "5000";
const URI = `${PROTOCOL}://${HOST_URL}:${HOST_PORT}`;

const PokerGameUI = () => {
  const pokerTableBackground = PokerTableBackground;
  const [players, setPlayers] = useState([]); // State for players
  const [playerPositions, setPlayerPositions] = useState([]);
  const [pot, setPot] = useState(null);
  const [communityCards, setCommunityCards] = useState([]);
  const [dealerIndex, setDealerIndex] = useState(null);

  const containerRef = useRef(null); // Reference to get container size

  // Update player positions based on container size
  const updatePlayerPositions = () => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      setPlayerPositions(getPlayerPositions(players.length, width, height));
    }
  };

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
        updatePlayerPositions(); // Update positions dynamically
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

  // Handle window resize for dynamic player positions
  useEffect(() => {
    const handleResize = () => {
      updatePlayerPositions();
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [players.length]); // Only re-run when the number of players changes

  useEffect(() => {
    updatePlayerPositions(); // Update positions after players are updated
  }, [players]);

  return (
    <div
      ref={containerRef} // Assign reference to the parent container for size measurement
      style={{ width: "100%", height: "100%", position: "relative", overflow: "hidden" }}
    >
      <PokerTable
        pokerTableBackground={pokerTableBackground}
        pot={pot !== null ? pot : "Loading..."}
      >
        {/* Render player components dynamically */}
        {players.map((player, index) => {
          const position = playerPositions[index];
          const isDealer = index === dealerIndex;
          return (
            position && ( // Only render if position is available
              <Player
                key={index}
                player={player}
                position={position}
                isDealer={isDealer}
              />
            )
          );
        })}

        {/* Render community cards */}
        <div
          style={{
            position: "absolute",
            top: "55%",
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
              style={{ width: "5.5vw", height: "auto" }}
            />
          ))}
        </div>
      </PokerTable>
    </div>
  );
};

export default PokerGameUI;