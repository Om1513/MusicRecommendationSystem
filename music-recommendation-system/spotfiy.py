import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd
import dotenv
import os
from bs4 import BeautifulSoup

# Load environment variables
dotenv.load_dotenv()

# Spotify API credentials
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')  # Genius API token

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private user-library-read"
))

# Function to search Genius for lyrics
def search_genius(song_name, artist_name):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {genius_access_token}"}
    search_url = f"{base_url}/search"
    params = {"q": f"{song_name} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        hits = response.json().get("response", {}).get("hits", [])
        if hits:
            # Return the URL of the first match
            return hits[0]["result"]["url"]
    return None

# Function to fetch lyrics from Genius
def fetch_lyrics(artist, song):
    lyrics_url = search_genius(song, artist)
    if lyrics_url:
        print(f"Lyrics URL: {lyrics_url}")
        lyrics_response = requests.get(lyrics_url)
        if lyrics_response.status_code == 200:
            soup = BeautifulSoup(lyrics_response.content, "html.parser")
            lyrics_div = soup.find("div", class_="lyrics")
            if lyrics_div:
                return lyrics_div.get_text(strip=True)
        return f"Lyrics available at: {lyrics_url}"  # Fall back to the URL
    return "Lyrics not found."

# Function to fetch songs from a Spotify playlist
def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            artist = track['artists'][0]['name']
            song = track['name']
            print(f"Fetching lyrics for: {song} by {artist}")
            lyrics = fetch_lyrics(artist, song)
            tracks.append({"artist": artist, "song": song, "text": lyrics})
        results = sp.next(results) if results['next'] else None
    return tracks

# Function to fetch liked songs and their lyrics
def get_liked_songs_with_lyrics():
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  # Adjust the limit if needed
    while results:
        for item in results["items"]:
            track = item["track"]
            artist = track["artists"][0]["name"]
            song = track["name"]
            print(f"Fetching lyrics for: {song} by {artist}")
            lyrics = fetch_lyrics(artist, song)
            liked_songs.append({"artist": artist, "song": song, "text": lyrics})
        results = sp.next(results) if results["next"] else None
    return liked_songs

# Save to CSV
def save_to_csv(data, filename="songs_with_lyrics.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Example Usage
if __name__ == "__main__":
    # Fetch songs from a specific playlist
    playlist_id = "your_playlist_id_here"  # Replace with actual playlist ID
    playlist_songs = get_playlist_tracks(playlist_id)
    save_to_csv(playlist_songs, filename="playlist_songs_with_lyrics.csv")

    # Fetch liked songs
    liked_songs = get_liked_songs_with_lyrics()
    save_to_csv(liked_songs, filename="liked_songs_with_lyrics.csv")


# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import dotenv
# import os


# dotenv.load_dotenv()

# # Debugging: Print loaded environment variables
# print("Client ID:", os.getenv('SPOTIPY_CLIENT_ID'))
# print("Client Secret:", os.getenv('SPOTIPY_CLIENT_SECRET'))
# print("Redirect URI:", os.getenv('SPOTIPY_REDIRECT_URI'))

# client_id = os.getenv('SPOTIPY_CLIENT_ID')
# client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
# redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# scope = "user-library-read"

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# playlists = sp.user_playlists('spotify')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None