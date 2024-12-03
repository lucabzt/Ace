import React, { useEffect, useState } from "react";
import './SlidePanel.css';

const SlidePanel = () => {
  const [player, setPlayer] = useState(null); // Spotify Player instance
  const [currentTrack, setCurrentTrack] = useState(null); // Currently playing track
  const [isPlaying, setIsPlaying] = useState(false); // Playback state
  const [deviceId, setDeviceId] = useState(null); // Spotify device ID

  // Retrieve the Spotify token (make sure it's saved after OAuth authentication)
  const token = localStorage.getItem("spotifyToken");

  useEffect(() => {
    if (!token) {
      console.error("Spotify token not found. Please authenticate.");
      return;
    }

    // Load Spotify Web Playback SDK
    const script = document.createElement("script");
    script.src = "https://sdk.scdn.co/spotify-player.js";
    script.async = true;
    document.body.appendChild(script);

    window.onSpotifyWebPlaybackSDKReady = () => {
      const spotifyPlayer = new window.Spotify.Player({
        name: "Poker App Spotify Player",
        getOAuthToken: (cb) => cb(token),
      });

      // Set up event listeners
      spotifyPlayer.addListener("ready", ({ device_id }) => {
        console.log("Player is ready with device ID", device_id);
        setDeviceId(device_id);
      });

      spotifyPlayer.addListener("not_ready", ({ device_id }) => {
        console.error("Device ID has gone offline", device_id);
      });

      spotifyPlayer.addListener("player_state_changed", (state) => {
        if (!state) return;
        setCurrentTrack(state.track_window.current_track);
        setIsPlaying(!state.paused);
      });

      // Connect the player
      spotifyPlayer.connect();
      setPlayer(spotifyPlayer);
    };

    return () => {
      document.body.removeChild(script); // Clean up script on unmount
    };
  }, [token]);

  // Play the default playlist
  const play = () => {
    fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_uri: "spotify:playlist:3GuG2wiCsxXEbc1hfFP3xn", // Default playlist URI from the provided link
      }),
    })
      .then((response) => {
        if (!response.ok) {
          console.error("Failed to play track", response.statusText);
        }
      })
      .catch((error) => console.error("Error playing track", error));
  };

  // Toggle playback between play and pause
  const togglePlay = () => {
    if (player) {
      player.togglePlay().catch((error) => console.error("Error toggling play:", error));
    }
  };

  return (
    <div className="slide-panel">
      <h2>Spotify Player</h2>
      {currentTrack ? (
        <div>
          <p>Now Playing: <strong>{currentTrack.name}</strong></p>
          <p>Artist: {currentTrack.artists.map(artist => artist.name).join(", ")}</p>
          <button className="spotify-button" onClick={togglePlay}>
            {isPlaying ? "Pause" : "Play"}
          </button>
        </div>
      ) : (
        <p>Loading player...</p>
      )}
      <button className="spotify-button" onClick={play}>
        Play Default Playlist
      </button>
    </div>
  );
};

export default SlidePanel;
