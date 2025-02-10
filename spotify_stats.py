import json
from pathlib import Path

class SongPlay:
    def __init__(self, artist, song_name, album, play_time):
        self.artist = artist
        self.song_name = song_name
        self.album = album
        self.play_time = play_time
        self.count = 1  # Initialize count to 1 when a song is first encountered

    def __repr__(self):
        return f"{self.song_name} by {self.artist} from album {self.album} (Playtime: {self.play_time}s, Listens: {self.count})"

    def __eq__(self, other):
        return self.song_name == other.song_name and self.artist == other.artist and self.album == other.album

    def __hash__(self):
        return hash((self.artist, self.song_name, self.album))

    def increment_count(self):
        self.count += 1

def read_json_files(directory):
    song_set = set()  # Set to store SongPlay objects

    # Get all the JSON files in the current directory
    json_files = Path(directory).glob("*.json")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            # For each song entry in the JSON file, add or update SongPlay object
            for entry in data:
                artist = entry.get("master_metadata_album_artist_name")
                song_name = entry.get("master_metadata_track_name")
                album = entry.get("master_metadata_album_album_name")
                play_time = entry.get("ms_played", 0)  # Default to 0 if no play_time provided
                
                # Check if we already have the song in the set
                existing_song = next((song for song in song_set if song.song_name == song_name and song.artist == artist and song.album == album), None)
                
                if existing_song:
                    # If song already exists, increment its count
                    existing_song.increment_count()
                else:
                    # If song doesn't exist, create a new SongPlay and add to set
                    new_song = SongPlay(artist, song_name, album, play_time)
                    song_set.add(new_song)
                
        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {e}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    return song_set

def main():
    directory = "."  # Current directory where the script is located
    
    song_set = read_json_files(directory)
    
    # Sort the songs by the number of listens in descending order
    sorted_songs = sorted(song_set, key=lambda song: song.count, reverse=True)
    
    # Print the top 50 most listened songs
    print("Top 50 most listened songs:")
    for i, song in enumerate(sorted_songs[:50]):
        print(f"{i + 1}. {song.song_name} by {song.artist} - {song.count} listens")

if __name__ == "__main__":
    main()
