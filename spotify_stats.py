import json
from pathlib import Path
from collections import defaultdict

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
    songs_dict = {}  # Key: song_name, artist, album | Value: SongPlay object
    artists_dict = defaultdict(int)  # Key: artist | Value: total listen count
    total_milliseconds_of_music = 0
    total_song_plays = 0
    # Get all the JSON files in the current directory
    json_files = Path(directory).glob("*.json")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            # For each song entry in the JSON file, add or update SongPlay object
            for entry in data:
                play_time = entry.get("ms_played", 0)  # Default to 0 if no play_time provided
                reason_end = entry.get("reason_end")

                # if a song was played for less than 30 seconds, don't count it as a listen
                if(play_time < 30000 and reason_end!="endplay"):
                    continue
                
                artist = entry.get("master_metadata_album_artist_name")
                song_name = entry.get("master_metadata_track_name")
                album = entry.get("master_metadata_album_album_name")

                if not artist or not song_name or not album:
                    continue

                total_milliseconds_of_music += play_time
                total_song_plays += 1
                
                # Update song dictionary with SongPlay object
                song_key = (song_name, artist, album)
                if song_key in songs_dict:
                    songs_dict[song_key].increment_count()
                else:
                    songs_dict[song_key] = SongPlay(artist, song_name, album, play_time)
                
                # Update artist listen count
                artists_dict[artist] += 1

        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {e}")
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    return songs_dict, artists_dict, total_milliseconds_of_music, total_song_plays

def main():
    directory = "."  # Current directory where the script is located
    
    songs_dict, artists_dict, total_milliseconds_of_music, total_song_plays = read_json_files(directory)
    
    # Sort the songs by the number of listens in descending order for output
    sorted_songs = sorted(songs_dict.values(), key=lambda song: song.count, reverse=True)
    
    # Sort the artists by the number of listens in descending order for output
    sorted_artists = sorted(artists_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Print the top 50 most listened songs
    print("Top 50 most listened songs:")
    for i, song in enumerate(sorted_songs[:50]):
        print(f"{i + 1}. {song.song_name} by {song.artist} - {song.count} listens")

    # Print the top 50 most listened artists
    print("\nTop 50 most listened artists:")
    for i, (artist, count) in enumerate(sorted_artists[:50]):
        print(f"{i + 1}. {artist} - {count} listens")

    print("\nTotal number of minutes listened: ", total_milliseconds_of_music / 60000)
    print("\nTotal number of song plays: ", total_song_plays)


if __name__ == "__main__":
    main()
