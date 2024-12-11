import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os

dotenv.load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')


genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

# Initialize Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-library-read"
))

def search_genius(song_name, artist_name):
    """
    Search for a song on Genius and fetch its lyrics.
    """
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {genius_access_token}"}
    search_url = f"{base_url}/search"
    params = {"q": f"{song_name} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        if hits:
            # Return the URL of the first match
            return hits[0]["result"]["url"]
    return None

def get_song_lyrics(song_name, artist_name):
    """
    Get lyrics of a song using Genius API.
    """
    lyrics_url = search_genius(song_name, artist_name)
    if lyrics_url:
        print(f"Lyrics URL: {lyrics_url}")
        return lyrics_url
    else:
        return "Lyrics not found."

def get_liked_songs_with_lyrics():
    """
    Fetch liked songs from Spotify and get their lyrics.
    """
    liked_songs = spotify.current_user_saved_tracks(limit=20)  # Fetch 10 liked songs for demo
    for item in liked_songs["items"]:
        track = item["track"]
        song_name = track["name"]
        artist_name = track["artists"][0]["name"]
        print(f"Fetching lyrics for: {song_name} by {artist_name}")
        lyrics = get_song_lyrics(song_name, artist_name)
        print(lyrics)
        print()

# Run the function
get_liked_songs_with_lyrics()
