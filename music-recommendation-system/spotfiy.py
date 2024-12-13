import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd
import dotenv
import os
from bs4 import BeautifulSoup
import re

dotenv.load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private user-library-read"
))

def search_genius(song_name, artist_name):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {genius_access_token}"}
    search_url = f"{base_url}/search"
    params = {"q": f"{song_name} {artist_name}"}
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        hits = response.json().get("response", {}).get("hits", [])
        if hits:
            return hits[0]["result"]["url"]
    return None

def fetch_lyrics_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
        if lyrics_divs:
            lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
            processed_lyrics = re.sub(r"[\[\]\\'\"]", "", lyrics)
            processed_lyrics = re.sub(r"\n", " ", processed_lyrics).strip()
            return processed_lyrics
    return "Lyrics not found."

def get_song_lyrics_text(song_name, artist_name):
    lyrics_url = search_genius(song_name, artist_name)
    if lyrics_url:
        return fetch_lyrics_from_url(lyrics_url)
    return "Lyrics not found."

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            artist = track['artists'][0]['name']
            song = track['name']
            print(f"Fetching lyrics for: {song} by {artist}")
            lyrics = get_song_lyrics_text(song, artist)
            tracks.append({"artist": artist, "song": song, "lyrics": lyrics})
        results = sp.next(results) if results['next'] else None
    return tracks

def get_liked_songs_with_lyrics():
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  
    while results:
        for item in results['items']:
            track = item['track']
            artist = track['artists'][0]['name']
            song = track['name']
            print(f"Fetching lyrics for: {song} by {artist}")
            lyrics = get_song_lyrics_text(song, artist)
            liked_songs.append({"artist": artist, "song": song, "lyrics": lyrics})
        results = sp.next(results) if results['next'] else None
    return liked_songs

def save_to_csv(data, filename="songs_with_lyrics.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    playlist_id = "https://open.spotify.com/playlist/6Qyc3GgiY7IXogHu2C43rn?si=PAE6yFHsQZCzFy8Qgk04iQ"  # Replace with actual playlist ID
    playlist_songs = get_playlist_tracks(playlist_id)
    save_to_csv(playlist_songs, filename="playlist_songs_with_lyrics.csv")

    # liked_songs = get_liked_songs_with_lyrics()
    # save_to_csv(liked_songs, filename="liked_songs_with_lyrics.csv")