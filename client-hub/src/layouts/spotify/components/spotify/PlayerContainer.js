import React, { useState, useEffect } from "react";
import axios from "axios";
import './PlayerContainer.css';

const PlayerContainer = () => {
  const [token, setToken] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [deviceId, setDeviceId] = useState(null);

  const PLAYLIST_URI = "spotify:playlist:3GuG2wiCsxXEbc1hfFP3xn"; // Hardcoded playlist URI

  useEffect(() => {
    // Extract token from URL hash
    const hash = window.location.hash;
    const tokenFromHash = hash
      .substring(1)
      .split("&")
      .find((elem) => elem.startsWith("access_token"))
      ?.split("=")[1];
    if (tokenFromHash) {
      setToken(tokenFromHash);
      localStorage.setItem("spotifyToken", tokenFromHash);
      window.location.hash = ""; // Clear token from URL
    }
  }, []);

  useEffect(() => {
    if (token) {
      const script = document.createElement("script");
      script.src = "https://sdk.scdn.co/spotify-player.js";
      script.async = true;
      document.body.appendChild(script);

      window.onSpotifyWebPlaybackSDKReady = () => {
        const player = new window.Spotify.Player({
          name: "React Spotify Player",
          getOAuthToken: (cb) => cb(token),
        });

        player.addListener("ready", ({ device_id }) => {
          setDeviceId(device_id);
        });

        player.addListener("player_state_changed", (state) => {
          if (state) {
            setCurrentTrack(state.track_window.current_track);
            setIsPlaying(!state.paused);
          }
        });

        player.connect();
      };
    }
  }, [token]);

  const playPlaylist = () => {
    if (!deviceId) {
      console.error("Device not ready");
      return;
    }
    axios
      .put(
        `https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`,
        {
          context_uri: PLAYLIST_URI,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      )
      .catch((error) => console.error("Error playing playlist:", error));
  };

  const togglePlay = () => {
    if (!token || !deviceId) return;

    axios
      .put(
        `https://api.spotify.com/v1/me/player/${isPlaying ? "pause" : "play"}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then(() => setIsPlaying(!isPlaying))
      .catch((error) => console.error("Error toggling play:", error));
  };

  return (
    <div className="slide-panel">
      <h2>Spotify Player</h2>
      {!token ? (
        <p>Please log in using Spotify to use the player.</p>
      ) : currentTrack ? (
        <div>
          <p>Now Playing: {currentTrack.name}</p>
          <p>Artist: {currentTrack.artists.map((artist) => artist.name).join(", ")}</p>
          <button onClick={togglePlay}>{isPlaying ? "Pause" : "Play"}</button>
        </div>
      ) : (
        <p>Loading player...</p>
      )}
      <button onClick={playPlaylist} disabled={!deviceId}>
        Play Default Playlist
      </button>
    </div>
  );
};

export default PlayerContainer;
