import lyricsgenius

# Your Genius API Access Token
genius = lyricsgenius.Genius("UUODLxcCpDdlIm_k8hqQvP-qYcQrfnvOB9ULnwDAS7LsQ-ZVtQwwJ7n-vUW-s2M3")


def divide_lyrics_into_chunks(lyrics, num_chunks):
    """Divide lyrics into a specified number of chunks."""
    lines = lyrics.split('\n')  # Split lyrics by lines
    chunk_size = len(lines) // num_chunks
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    return chunks


def generate_karaoke_timeline(lyrics, total_duration, num_chunks=5):
    """Generate timeline for displaying lyrics."""
    chunks = divide_lyrics_into_chunks(lyrics, num_chunks)
    interval_duration = total_duration / num_chunks
    timeline = []
    current_time = 0

    for chunk in chunks:
        timeline.append({
            "time": current_time,
            "lyrics": '\n'.join(chunk)
        })
        current_time += interval_duration

    return timeline


def get_song_lyrics_and_karaoke_timeline(artist_name, song_title, song_duration):
    """Fetch lyrics and generate a karaoke timeline."""
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            lyrics = song.lyrics
            karaoke_timeline = generate_karaoke_timeline(lyrics, song_duration)
            return karaoke_timeline
        else:
            return "Lyrics not found."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    artist = input("Enter the artist's name: ")
    title = input("Enter the song title: ")
    duration = int(input("Enter the song duration in seconds: "))

    timeline = get_song_lyrics_and_karaoke_timeline(artist, title, duration)

    print("\nKaraoke Timeline:\n")
    if isinstance(timeline, str):
        print(timeline)
    else:
        for entry in timeline:
            print(f"Time: {entry['time']}s")
            print(entry['lyrics'])
            print("\n---\n")