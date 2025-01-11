import React, { useState, useEffect, useRef } from "react";
import Player from "../player/Player";
import PokerTable from "../PokerTable";
import { getPlayerPositions } from "../../utils/positionUtils";
import { loadCardImage } from "../../utils/cardUtils";
import PokerTableBackground from "../../../../assets/images/poker/poker_table/PokerTable100.png";

// Import von lineChartDataDashboard
import { lineChartDataDashboard } from "../../../dashboard/data/lineChartData";

const serverAddress = "https://localhost:5000";
console.log("Server Address:", serverAddress);

const PokerGameUI = () => {
  const pokerTableBackground = PokerTableBackground;
  const [players, setPlayers] = useState([]); // State for players
  const [playerPositions, setPlayerPositions] = useState([]);
  const [pot, setPot] = useState(null);
  const [communityCards, setCommunityCards] = useState([]);
  const [dealerIndex, setDealerIndex] = useState(null);
  const containerRef = useRef(null); // Reference to get container size

  let syncCallCount = 0; // Zähler für Aufrufe von syncChartDataWithPlayers

  // Funktion zum Synchronisieren von Spielern und lineChartDataDashboard + Balance-Pushing
  const syncChartDataWithPlayers = (players) => {
    players.forEach((player) => {
      const playerData = lineChartDataDashboard.find(
        (data) => data.name === player.name
      );
      let serverPnlData = player.pnl || []; // PnL-Daten des Servers für den Spieler
      if (!playerData) {
        // Spieler zu den Chart-Daten hinzufügen, falls er nicht existiert
        lineChartDataDashboard.push({
          name: player.name,
          data: serverPnlData, // Alle PnL-Daten vom Server übernehmen
        });
        console.log(`New player added to chart: ${player.name}`);
      } else {
        // Fehlen noch Einträge, die noch nicht hinzugefügt wurden?
        const existingTimestamps = new Set(playerData.data.map((d) => d[0])); // Zeitstempel im Frontend
        serverPnlData.forEach(([timestamp, pnl]) => {
          if (!existingTimestamps.has(timestamp)) {
            // Nur neue Datenpunkte hinzufügen
            playerData.data.push([timestamp, pnl]);
            console.log(`Chart: New data point added for player: ${player.name} | Timestamp: ${timestamp}, PnL: ${pnl}`);
          }
        });
      }
      // console.log(`Chart updated for player: ${player.name}`);
    });
  };
  // Update player positions based on container size
  const updatePlayerPositions = () => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      setPlayerPositions(getPlayerPositions(players.length, width, height));
    }
  };

  // Fetch player data
  const fetchPlayers = () => {
    fetch(`${serverAddress}/players`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch players data");
        }
        return res.json();
      })
      .then((data) => {
        setPlayers(data);

        syncCallCount++; // Zähler inkrementieren
        if (syncCallCount >= 10) {
          syncChartDataWithPlayers(data); // Synchronisieren mit den Chart-Daten
          syncCallCount = 0; // Zähler zurücksetzen
        }
        updatePlayerPositions(); // Update positions dynamically
        //console.log("Players data updated:", data);
      })
      .catch((error) => console.error("Error fetching players data:", error));
  };

  // Polling logic for other game data
  const pollGameData = () => {
    fetch(`${serverAddress}/pot`)
      .then((res) => res.json())
      .then((data) => setPot(data.pot))
      .catch((error) => console.error("Error fetching pot value:", error));

    fetch(`${serverAddress}/community-cards`)
      .then((res) => res.json())
      .then((data) => setCommunityCards(data))
      .catch((error) => console.error("Error fetching community cards:", error));

    fetch(`${serverAddress}/dealer`)
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
    }, 1000);
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
              style={{ width: "5.5vw", height: "auto" }}
            />
          ))}
        </div>
      </PokerTable>
    </div>
  );
};

export default PokerGameUI;