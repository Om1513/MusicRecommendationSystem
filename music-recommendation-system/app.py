import pickle
import time
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

dotenv.load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read playlist-read-private"
)

sp = None  # Placeholder for Spotify client

def login_to_spotify():
    global sp
    if not sp:  # Initialize only if not already initialized
        token_info = sp_oauth.get_access_token(as_dict=False)
        sp = spotipy.Spotify(auth=token_info)

def get_song_album_cover_url(song_name, artist_name):
    global sp
    if not sp:  # Ensure the Spotify client is initialized
        login_to_spotify()
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

def get_user_playlists():
    global sp
    if not sp:  # Ensure the Spotify client is initialized
        login_to_spotify()
    playlists = sp.current_user_playlists()
    playlist_data = {playlist['name']: playlist['id'] for playlist in playlists['items']}
    return playlist_data

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

# Navigation state
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Render buttons in the navbar
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("Home", key="home-button"):
        st.session_state["page"] = "Home"

with col2:
    if st.button("User Playlist", key="user-playlist-button"):
        st.session_state["page"] = "User Playlist"

with col3:
    if st.button("Documentation", key="documentation-button"):
        st.session_state["page"] = "Documentation"

with col4:
    if st.button("About", key="about-button"):
        st.session_state["page"] = "About"
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: rgb(14, 17, 23);
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        border: 0px solid white;
    }
    .stButton > button:hover {
        background-color: white;
        color: black;
        border-color: white;
    }
    .page > button {
        background-color: #14833b ;
        color: white;
        border-color: white ;
    }
        .navbar-divider {
        border-top: 2px solid white;
    }
        .song-container {
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .song-container:hover {
        transform: scale(1.3); /* Zoom-in effect */
    }
    .song-poster {
        width: 100%;
        border-radius: 8px;
    }
    .song-name {
        margin-top: 8px;
        font-size: 14px;
        font-weight: bold;
        color: white;
    }
    </style>
    <div class="navbar-divider"></div>""",
    unsafe_allow_html=True,
)
# Render the selected page
if st.session_state['page'] == "Home":
    st.header('Home - Music Recommendation System')
    music = pd.read_csv('spotify_millsongdata.csv')
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    st.subheader("Music Recommender for our Dataset")

    music_list = music['song'].values
    selected_song = st.selectbox(
        "Type or select a song from the dropdown",
        music_list
    )

    if st.button('Show Recommendation', key='recommendation-button'):
        recommended_music_names, recommended_music_posters = recommend(selected_song)
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, (col, name, poster) in enumerate(zip([col1, col2, col3, col4, col5], recommended_music_names, recommended_music_posters)):
            with col:
                st.markdown(
                    f"""
                    <div class="song-container" id="song-{i}">
                        <img class="song-poster" src="{poster}" alt="Poster">
                        <p class="song-name">{name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
elif st.session_state['page'] == "User Playlist":
    st.header('Playlist-Based Music Recommender System')

    # Login Page
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.subheader("Login with your Spotify account")
        if st.button("Login", key="login-button"):
            try:
                with st.spinner('Logging in...'):
                    time.sleep(1)
                    login_to_spotify()
                    st.session_state['logged_in'] = True
                st.success("Successfully logged in! Redirecting to the music recommender...")
                st.rerun()  # Redirect to the recommender
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
    else:
        st.subheader("Your Spotify Playlists")
        playlists = get_user_playlists()
        playlist_names = list(playlists.keys())
        selected_playlist = st.selectbox("Select a playlist to view recommendations", playlist_names)

        # Display selected playlist and its ID
        if selected_playlist:
            st.write(f"Selected Playlist: {selected_playlist}")

            # playlist_songs = get_playlist_tracks(playlists[selected_playlist])
            # save_to_csv(playlist_songs, filename="playlist_songs_with_lyrics.csv")
        music = pd.read_csv('cleaned_playlist_songs_with_lyrics.csv')
        similarity = pickle.load(open('similarityplay.pkl', 'rb'))

        st.subheader("Music Recommender")

        music_list = music['song'].values
        selected_song = st.selectbox(
            "Type or select a song from the dropdown",
            music_list
        )

        if st.button('Show Recommendation'):
            recommended_music_names, recommended_music_posters = recommend(selected_song)
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, (col, name, poster) in enumerate(zip([col1, col2, col3, col4, col5], recommended_music_names, recommended_music_posters)):
                with col:
                    st.markdown(
                        f"""
                        <div class="song-container" id="song-{i}">
                            <img class="song-poster" src="{poster}" alt="Poster">
                            <p class="song-name">{name}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

elif st.session_state['page'] == "Documentation":
    st.header("Documentation")
    st.write("Find the complete documentation [here](https://github.com/Om1513/MusicRecommendationSystem).")

elif st.session_state['page'] == "About":
    st.header("About This Project")
    st.write(
        """
        This Music Recommendation System integrates Spotify's API and a pre-trained similarity model to provide personalized music recommendations.
        The system features playlist-based recommendations and lyrics analysis, offering an engaging and dynamic user experience.
        """
    )
