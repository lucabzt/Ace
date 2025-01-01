import React, { useEffect, useState, useRef } from "react";

import "./SpotifyPlayer.css"
import {BsPauseFill, BsPlayFill, BsSkipBackwardFill, BsSkipForwardCircleFill, BsSkipForwardFill} from "react-icons/bs";
import {FiSkipForward} from "react-icons/fi";


const SpotifyPlayer = ({ token, refreshToken, expiresAt }) => {
  //const [player, setPlayer] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [trackDuration, setTrackDuration] = useState(0); // Track duration in milliseconds
  const player = useRef(null);
  const [currentToken, setCurrentToken] = useState(token);
  const [expirationTime, setExpirationTime] = useState(expiresAt);

  const refreshAccessToken = async () => {
    try {
      const response = await fetch(
        `/refresh_token?refresh_token=${refreshToken}`
      );
      if (response.ok) {
        const data = await response.json();
        const newToken = data.access_token;
        const newExpiresIn = data.expires_in; // Seconds

        // Update token and expiration time
        setCurrentToken(newToken);
        setExpirationTime(Date.now() + newExpiresIn * 1000); // Convert to ms
      } else {
        console.error("Failed to refresh token:", response.statusText);
      }
    } catch (err) {
      console.error("Error refreshing token:", err);
    }
  };

  
  useEffect(() => {
    // Check token expiration periodically
    const interval = setInterval(() => {
      if (Date.now() >= expirationTime - 60000) {
        // Refresh token 1 minute before it expires
        refreshAccessToken();
      }
    }, 5000); // Check every 5 seconds

    return () => clearInterval(interval);
  }, [expirationTime]);

  // Pass updated token to Spotify Web Playback SDK
  useEffect(() => {
    if (currentToken) {
      console.log("Updated token for SDK:", currentToken);
    }
  }, [currentToken]);

  


  const [trackProgress, setTrackProgress] = useState(0); // Current progress in milliseconds
  useEffect(() => {
    const interval = setInterval(updateProgress, 1000); // Update progress every second
    return () => clearInterval(interval);
  }, [isPlaying]);



  const skipToNext = () => {
    if (player.current) {
      player.current.nextTrack().catch((err) => console.error("Next track error:", err));
    }
  };

  const skipToPrevious = () => {
    if (player.current) {
      player.current.previousTrack().catch((err) => console.error("Previous track error:", err));
    }
  };



  const updateProgress = () => {
    if (player.current && isPlaying) {
      player.current.getCurrentState().then((state) => {
        if (state) {
          setTrackProgress(state.position);
        }
      });
    }
  };


  const startPlaylistPlayback = (id) => {
    fetch(`https://api.spotify.com/v1/me/player/play?device_id=${id}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_uri: "spotify:playlist:3GuG2wiCsxXEbc1hfFP3xn", // Replace with your playlist URI
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to start playlist playback: ${response.statusText}`);
        }
        console.log("Playlist playback started successfully!");
      })
      .catch((err) => {
        console.error("Error starting playlist playback:", err);
      });
  };



  useEffect(() => {
    if (!token)
         return;    
    if (token) {
      console.log("useEffect: token = " + token);
      console.log("A");

      const script = document.createElement("script");
      script.src = "https://sdk.scdn.co/spotify-player.js";
      script.async = true;
      document.body.appendChild(script);

      window.onSpotifyWebPlaybackSDKReady = () => {
        const spotifyPlayer = new window.Spotify.Player({
          name: "React Spotify Player",
          getOAuthToken: (cb) => cb(token),
        });

        spotifyPlayer.addListener("ready", ({ device_id }) => {
          console.log("Ready with Device ID:", device_id);
          startPlaylistPlayback(device_id);
        });

        spotifyPlayer.addListener("player_state_changed", (state) => {
          if (state) {
            const track = state.track_window.current_track;
            setCurrentTrack(track);
            setIsPlaying(!state.paused);
            setTrackDuration(track.duration_ms);
            setTrackProgress(state.position);
          }
        });

        spotifyPlayer.connect();
        //setPlayer(spotifyPlayer);
        player.current = spotifyPlayer; // Use ref instead of state
      };
      console.log("AB");

      return () => {
        if (player) {
            player.current.disconnect(); // Disconnect player
        }
        document.body.removeChild(script);
      };

    }
  }, [token]);

   // Disconnect the player on logout
   const handlePlayerDisconnect = () => {
    if (player) {
      player.current.disconnect();
    }
    localStorage.removeItem("spotifyAccessToken"); // Remove token from storage
  };

  const togglePlay = () => {
    if (player) {
      player.current.togglePlay().catch((err) => console.error("Toggle play error:", err));
    }
  };

  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };


  
  const progressPercentage = (trackProgress / trackDuration) * 100 || 0;
  
  return (
    <div className="spotify-player-container">
      {currentTrack ? (
        <div className="track-info">
          <img
            src={currentTrack.album.images[0].url}
            alt={currentTrack.name}
            className="track-image"
          />
          <div className="track-details">
            <p className="track-name"><strong>{currentTrack.name}</strong></p>
            <p className="track-artist">{currentTrack.artists.map((a) => a.name).join(", ")}</p>
            <p className="track-duration">
              {formatDuration(trackProgress)} / {formatDuration(trackDuration)}
            </p>
            <div className="progress-bar-container">
              <div
                className="progress-bar"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <div className="button-container"> {/* Neue Klasse hinzugefügt */}
              <button className="play-pause-button" onClick={skipToPrevious}>
                <BsSkipBackwardFill size="25px" color="inherit"/>
              </button>
              <button className="play-pause-button" onClick={togglePlay}>
                {isPlaying ? (
                    <BsPauseFill size="25px" color="inherit"/>
                ) : (
                    <BsPlayFill size="25px" color="inherit"/>
                )}
              </button>
              <button className="play-pause-button" onClick={skipToNext}>
                <BsSkipForwardFill size="25px" color="inherit"/>
              </button>
            </div>
          </div>
        </div>
      ) : (
          <p>Loading Player...</p>
      )}
    </div>
  );
};

export default SpotifyPlayer;
