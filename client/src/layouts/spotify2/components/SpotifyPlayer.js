
import React, { useEffect, useRef, useState } from "react";
import "./SpotifyPlayer.css";
import { useSpotify } from "./SpotifyContext";
import {
  BsPauseFill,
  BsPlayFill,
  BsSkipBackwardFill,
  BsSkipForwardFill,
} from "react-icons/bs";
import { PiShuffleBold } from "react-icons/pi";

const SpotifyPlayer = ({useLyrics }) => {
  //const [player, setPlayer] = useState(null);
  const { token } = useSpotify();
  const player = useRef(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const [trackDuration, setTrackDuration] = useState(0);
  const [isShuffle, setShuffleState] = useState(false);
  const [deviceID, setDeviceID] = useState(null);
  const [lyrics, setLyrics] = useState("");
  const [loadingLyrics, setLoadingLyrics] = useState(false);


  useEffect(() => {
    if (!token) return;

    const script = document.createElement("script");
    script.src = "https://sdk.scdn.co/spotify-player.js";
    script.async = true;
    document.body.appendChild(script);

    window.onSpotifyWebPlaybackSDKReady = () => {
      const spotifyPlayer = new window.Spotify.Player({
        name: "Spotify Web Player",
        getOAuthToken: (cb) => cb(token),
      });

      spotifyPlayer.addListener("ready", ({ device_id }) => {
        console.log("Ready with Device ID:", device_id);
      });

      spotifyPlayer.addListener("player_state_changed", (state) => {
        if (state) {
          setCurrentTrack(state.track_window.current_track);
          setIsPlaying(!state.paused);
          setTrackDuration(state.track_window.current_track.duration_ms);
          setTrackProgress(state.position);
        }
      });

      spotifyPlayer.addListener("ready", ({ device_id }) => {
        setDeviceID(device_id); // Store device ID for playback and shuffle
        console.log("Ready with Device ID:", device_id);
      });

      spotifyPlayer.connect();
      player.current = spotifyPlayer;
    };

    return () => {
      player.current?.disconnect();
      document.body.removeChild(script);
    };
  }, [token]);

  const togglePlay = () => {
        if (player) {
      if (currentTrack === null) {
        console.log("currentTrack is null: ", deviceID);
        startPlaylistPlayback(deviceID);
        return
      } else {
        player.current.togglePlay().catch((err) => console.error("Toggle play error:", err));
      }
    }
  };


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
    console.log("Starting playlist playback..." + token + " deviceID: " + id);
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

  // Disconnect the player on logout
  const handlePlayerDisconnect = () => {
    if (player) {
      player.current.disconnect();
    }
    localStorage.removeItem("spotifyAccessToken"); // Remove token from storage
  };

  const setShuffle = () => {
    setShuffleState(!isShuffle);
    fetch(`https://api.spotify.com/v1/me/player/shuffle?device_id=${deviceID}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`, // your OAuth token
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state: isShuffle,  // Set to `true` for shuffle, `false` to turn off shuffle
      }),
    })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to set shuffle state: ${response.statusText}`);
          }
          console.log(`Shuffle ${isShuffle ? "enabled" : "disabled"}`);
        })
        .catch((err) => {
          console.error("Error setting shuffle:", err);
        });
  };

  
  const fetchLyrics = (artist, title) => {
  // Use only the first artist, if multiple artists exist
  const formattedArtist = artist.includes(",") ? artist.split(",")[0] : artist;

  // Remove " - " and everything after it in the title (if present)
  const formattedTitle = title.includes(" - ") ? title.split(" - ")[0] : title;

  setLoadingLyrics(true); // Set loading state

  fetch(
    `https://localhost:5000/lyrics?artist=${encodeURIComponent(
      formattedArtist.trim() // Ensure no leading/trailing spaces
    )}&title=${encodeURIComponent(formattedTitle.trim())}`
  )
    .then((res) => {
      if (!res.ok) {
        throw new Error("Failed to fetch lyrics");
      }
      return res.json();
    })
    .then((data) => {
      if (data.error) {
        console.error("Error fetching lyrics:", data.error);
        setLyrics("Lyrics not found for this track.");
      } else {
        setLyrics(data.lyrics);
        //console.log("Fetched Lyrics:", data.lyrics); // Output lyrics to console
      }
    })
    .catch((err) => {
      console.error("Error fetching lyrics:", err);
      setLyrics("An error occurred while fetching lyrics.");
    })
    .finally(() => {
      setLoadingLyrics(false); // Reset loading state
    });
};

  useEffect(() => {
    if (currentTrack) {
      // Prüft, wenn sich der Track (Name/ID) ändert:
      const artist = currentTrack.artists.map((a) => a.name).join(", ");
      const title = currentTrack.name;
      fetchLyrics(artist, title); // Ruft Lyrics nur bei Änderung des Tracks ab.
    }
  // Nur ausführen wenn sich der currentTrack ändert.
  }, [currentTrack]);

  const progressPercentage = (trackProgress / trackDuration) * 100 || 0;
  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

return (
  <div className="spotify-player-container">
    {player ? (
      <>
        {/* Left side: Song playback */}
        <div className="playback-container">
          <div className="track-info">
            {currentTrack ? (
              <img
                src={currentTrack.album.images[0].url}
                alt={currentTrack.name}
                className="track-image"
              />
            ) : (
              <img
                src="https://image-cdn-ak.spotifycdn.com/image/ab67706c0000d72cdd7cb0d442bee004f48dee14"
                alt="Placeholder"
                className="track-image"
              />
            )}
            <div className="track-details">
              {currentTrack ? (
                <div>
                  <p className="track-name">
                    <strong>{currentTrack.name}</strong>
                  </p>
                  <p className="track-artist">
                    {currentTrack.artists.map((a) => a.name).join(", ")}
                  </p>
                </div>
              ) : (
                <div></div>
              )}
              <p className="track-duration">
                {formatDuration(trackProgress)} / {formatDuration(trackDuration)}
              </p>
              <div className="progress-bar-container">
                <div
                  className="progress-bar"
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
              <div className="button-container">
                <button className="play-pause-button" onClick={skipToPrevious}>
                  <BsSkipBackwardFill size="25px" color="inherit" />
                </button>
                <button className="play-pause-button" onClick={togglePlay}>
                  {isPlaying ? (
                    <BsPauseFill size="25px" color="inherit" />
                  ) : (
                    <BsPlayFill size="25px" color="inherit" />
                  )}
                </button>
                <button className="play-pause-button" onClick={skipToNext}>
                  <BsSkipForwardFill size="25px" color="inherit" />
                </button>
                <button
                  className={`play-pause-button ${
                    isShuffle ? "is-shuffle-active" : ""
                  }`}
                  onClick={setShuffle}
                >
                  <PiShuffleBold size="25px" color="inherit" />
                </button>
              </div>
            </div>
          </div>
        </div>
        {/* Right side: Lyrics */}
        {(useLyrics) ? (
        <div className="lyrics-container">
          <h3>Lyrics:</h3>
          {loadingLyrics ? (
            <p>Loading lyrics...</p>
          ) : (
            <div className="lyrics-box">
              <pre className="lyrics-text">{lyrics}</pre>
            </div>
          )}
        </div>) : (<> </>)}
      </>
    ) : (
      <p>Loading Player...</p>
    )}
  </div>
);
};

export default SpotifyPlayer;
