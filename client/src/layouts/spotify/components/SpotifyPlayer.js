import React, { useEffect, useState, useRef } from "react";

import "./SpotifyPlayer.css"
import {
  BsPauseFill,
  BsPlayFill,
  BsSkipBackwardFill,
  BsSkipForwardFill,
} from "react-icons/bs";
import {PiShuffleBold} from "react-icons/pi";
import { BsFillVolumeMuteFill } from "react-icons/bs";
import {BiSolidVolumeFull} from "react-icons/bi";
import { ImVolumeHigh, ImVolumeLow, ImVolumeMedium, ImVolumeMute2 } from "react-icons/im";

const SpotifyPlayer = ({ token, refreshToken, expiresAt, useLyrics }) => {
  //const [player, setPlayer] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [trackDuration, setTrackDuration] = useState(0); // Track duration in milliseconds
  const player = useRef(null);
  const [currentToken, setCurrentToken] = useState(token);
  const [expirationTime, setExpirationTime] = useState(expiresAt);
  const [deviceID, setDeviceID] = useState(null);
  const [isShuffle, setShuffleState] = useState(true);
  const [lyrics, setLyrics] = useState(null); // Lyrics state
  const [loadingLyrics, setLoadingLyrics] = useState(false); // Loading state for lyrics
  const [trackId, setTrackId] = useState(null); // Add trackId state
  const [volume, setVolume] = useState(100); // Default volume 100%
  const [isMuted, setIsMuted] = useState(false);
  const lyricsContainerRef = useRef(null); // Ref for the lyrics container
  const [isAutoScrolling, setIsAutoScrolling] = useState(false); // Track if auto-scroll is active

  useEffect(() => {
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

    // Check token expiration periodically
    const interval = setInterval(() => {
      if (Date.now() >= expirationTime - 60000) {
        // Refresh token 1 minute before it expires
        refreshAccessToken();
      }
    }, 5000); // Check every 5 seconds

    return () => clearInterval(interval);
  }, [expirationTime, refreshToken]);

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

  async function checkShuffleState() {
    const url = "https://api.spotify.com/v1/me/player";

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            console.error(`Error: ${response.status} - ${response.statusText}`);
            return;
        }

        const data = await response.json();

        // Check if shuffle_state exists and is true
        if (data && typeof data.shuffle_state === "boolean") {
            if (data.shuffle_state === true) {
                console.log("Shuffle is enabled.");
                setShuffleState(true);
            } else {
                console.log("Shuffle is disabled.");
                setShuffleState(false);
            }
            return data.shuffle_state; // Returns true if enabled, false if not
        } else {
            console.error("shuffle_state not found in the response.");
            return null;
        }
    } catch (error) {
        console.error("Failed to fetch playback state:", error.message);
        return null;
    }
}


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

  const setPlaylistContext = (deviceId, playlistUri, spotifyPlayer) => {
    fetch(`https://api.spotify.com/v1/me/player`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        device_ids: [deviceId],
        context_uri: playlistUri, // Playlist URI
      }),
    })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to set playlist context: ${response.statusText}`);
          }
          console.log("Playlist context set successfully!");
          checkShuffleState();
        })
        .catch((err) => {
          console.error("Error setting playlist context:", err);
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

        /*spotifyPlayer.addListener("ready", ({ device_id }) => {
          console.log("Ready with Device ID:", device_id);
          startPlaylistPlayback(device_id);
        });
        */


        spotifyPlayer.addListener("ready", ({device_id}) => {
          console.log("Ready with Device ID:", device_id);
          //startPlaylistPlayback(device_id, "spotify:playlist:3GuG2wiCsxXEbc1hfFP3xn", spotifyPlayer);
          setDeviceID(device_id);
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

  const setShuffle = () => {
    setShuffleState(!isShuffle);

    console.log("set shuffle state to: ", isShuffle, " token: ", token, " deviceID: ", deviceID);

    fetch(`https://api.spotify.com/v1/me/player/shuffle?state=${isShuffle}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`, // your OAuth token
      }
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

  const handleVolumeChange = (e) => {
  const newVolume = parseInt(e.target.value);
  setVolume(newVolume);
  if (player.current) {
    player.current.setVolume(newVolume / 100); // Spotify expects 0-1
  }
  if (isMuted && newVolume > 0) setIsMuted(false);
};

  const toggleMute = () => {
  if (isMuted) {
    player.current.setVolume(volume / 100);
  } else {
    player.current.setVolume(0);
  }
  setIsMuted(!isMuted);
};

  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

const fetchLyrics = (artist, title) => {
  const formattedArtist = artist.includes(",") ? artist.split(",")[0] : artist;
  const formattedTitle = title.includes(" - ") ? title.split(" - ")[0] : title;

  setLoadingLyrics(true);

  fetch(
    `https://localhost:5000/lyrics?artist=${encodeURIComponent(
      formattedArtist.trim()
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
        const currentArtists = currentTrack.artists.map((a) => a.name.toLowerCase());
        const fetchedArtist = data.artist.toLowerCase();

        //if (!currentArtists.includes(fetchedArtist)) {
          // Fetched lyrics belong to an outdated song, fetch again for the correct track
          //const newArtist = currentTrack.artists.map((a) => a.name).join(", ");
          //const newTitle = currentTrack.name;
          //fetchLyrics(newArtist, newTitle);
        //} else {
          setLyrics(data.lyrics);
        //}
      }
    })
    .catch((err) => {
      console.error("Error fetching lyrics:", err);
      setLyrics("An error occurred while fetching lyrics... ¯\\_(ツ)_/¯\n" +
          "\n" +
          "Maybe this song doesn't have any lyrics after all?");
    })
    .finally(() => {
      setLoadingLyrics(false);
    });
};

  useEffect(() => {
    if (currentTrack) {
      const { id } = currentTrack;
      if (id !== trackId) {
        // Update trackId only if it's a new track
        setTrackId(id);
      }
    }
  }, [currentTrack]);

  useEffect(() => {
  if (trackId) {
    const artist = currentTrack.artists.map((a) => a.name).join(", ");
    const title = currentTrack.name;
    fetchLyrics(artist, title); // Fetch lyrics for the new track
  }
}, [trackId]);

  const getVolumeIcon = (volume, isMuted) => {
    if (isMuted || volume === 0) return <ImVolumeMute2 size="25px" />;
    if (volume <= 33) return <ImVolumeLow size="25px" />;
    if (volume <= 66) return <ImVolumeMedium size="25px" />;
    return <ImVolumeHigh size="25px" />;
  };

   useEffect(() => {
    let scrollInterval;
    let startScrollTimeout;

    if (lyrics && trackDuration > 0) {
      // Start auto-scroll 10 seconds into the song
      startScrollTimeout = setTimeout(() => {
        setIsAutoScrolling(true);

        const container = lyricsContainerRef.current;
        if (!container) return;

        const scrollHeight = container.scrollHeight - container.clientHeight; // Total scrollable height
        const scrollDuration = trackDuration - 40000; // Time for scrolling (ms)

        // Calculate scroll speed (pixels/ms)
        const scrollSpeed = scrollHeight / scrollDuration;

        scrollInterval = setInterval(() => {
          if (isPlaying && container) {
            const currentScrollTop = container.scrollTop;
            const newScrollTop = currentScrollTop + scrollSpeed * 200;

            // Scroll until the end of the container
            if (newScrollTop < scrollHeight) {
              container.scrollTo({
                top: newScrollTop,
                behavior: "smooth",
              });
            } else {
              clearInterval(scrollInterval); // Stop scrolling at the end
            }
          }
        }, 50); // Update scroll position every second
      }, 20000); // Start after 10 seconds
    }

    return () => {
      clearTimeout(startScrollTimeout);
      clearInterval(scrollInterval);
    };
  }, [lyrics, trackDuration, isPlaying]);



  const progressPercentage = (trackProgress / trackDuration) * 100 || 0;

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
                    style={{width: `${progressPercentage}%`}}
                ></div>
              </div>
              <div className="button-container">
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
                <button className={`play-pause-button ${
                        isShuffle ? "" : "is-shuffle-active"
                    }`}
                    onClick={setShuffle}
                >
                  <PiShuffleBold size="25px" color="inherit"/>
                </button>
              </div>
              {/* Volume Controls */}
              <div className="volume-container">
                <button className="volume-button" onClick={toggleMute}>
                  {getVolumeIcon(volume, isMuted)}
                </button>
                <input
                    type="range"
                    min="0"
                    max="100"
                    value={volume}
                    onChange={handleVolumeChange}
                    className="volume-slider"
                    style={{'--fill-level': `${volume}%`}}
                />
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
              <div ref={lyricsContainerRef} className="lyrics-box" >
                <pre className="lyrics-text">{lyrics}</pre>
              </div>
          )}
                </div>) :
            (<> </>)
        }
      </>
    ) : (
        <p>Loading Player...</p>
    )}
  </div>
);
};

export default SpotifyPlayer;
