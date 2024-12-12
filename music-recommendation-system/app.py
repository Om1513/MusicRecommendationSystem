import pickle
import time
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os
import pandas as pd

dotenv.load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

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

# Navigation state
if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

# Navbar with buttons in a row
col1, col2, col3,col4 = st.columns(4)

with col1:
    if st.button("Home"):
        st.session_state['page'] = "Home"

with col2:
    if st.button("User Playlist"):
        st.session_state['page'] = "User Playlist"

with col3:
    if st.button("Documentation"):
        st.session_state['page'] = "Documentation"
with col4:
    if st.button("About"):
        st.session_state['page'] = "About"

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
        with col1:
            st.text(recommended_music_names[0])
            st.image(recommended_music_posters[0])
        with col2:
            st.text(recommended_music_names[1])
            st.image(recommended_music_posters[1])

        with col3:
            st.text(recommended_music_names[2])
            st.image(recommended_music_posters[2])
        with col4:
            st.text(recommended_music_names[3])
            st.image(recommended_music_posters[3])
        with col5:
            st.text(recommended_music_names[4])
            st.image(recommended_music_posters[4])
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
        music = pd.read_csv('playlist_songs_with_lyrics.csv')
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
            with col1:
                st.text(recommended_music_names[0])
                st.image(recommended_music_posters[0])
            with col2:
                st.text(recommended_music_names[1])
                st.image(recommended_music_posters[1])

            with col3:
                st.text(recommended_music_names[2])
                st.image(recommended_music_posters[2])
            with col4:
                st.text(recommended_music_names[3])
                st.image(recommended_music_posters[3])
            with col5:
                st.text(recommended_music_names[4])
                st.image(recommended_music_posters[4])
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

# import pickle
# import time
# import streamlit as st
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import dotenv
# import os
# import pandas as pd

# dotenv.load_dotenv()

# CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
# REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# sp_oauth = SpotifyOAuth(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET,
#     redirect_uri=REDIRECT_URI,
#     scope="user-library-read playlist-read-private"
# )

# sp = None  # Placeholder for Spotify client

# def login_to_spotify():
#     global sp
#     if not sp:  # Initialize only if not already initialized
#         token_info = sp_oauth.get_access_token(as_dict=False)
#         sp = spotipy.Spotify(auth=token_info)

# def get_song_album_cover_url(song_name, artist_name):
#     global sp
#     if not sp:  # Ensure the Spotify client is initialized
#         login_to_spotify()
#     search_query = f"track:{song_name} artist:{artist_name}"
#     results = sp.search(q=search_query, type="track")

#     if results and results["tracks"]["items"]:
#         track = results["tracks"]["items"][0]
#         album_cover_url = track["album"]["images"][0]["url"]
#         return album_cover_url
#     else:
#         return "https://i.postimg.cc/0QNxYz4V/social.png"

# def recommend(song):
#     index = music[music['song'] == song].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_music_names = []
#     recommended_music_posters = []
#     for i in distances[1:6]:
#         artist = music.iloc[i[0]].artist
#         recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
#         recommended_music_names.append(music.iloc[i[0]].song)

#     return recommended_music_names, recommended_music_posters

# st.header('Music Recommendation System')
# music = pd.read_csv('spotify_millsongdata.csv')
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# st.subheader("Music Recommender for our Dataset")

# music_list = music['song'].values
# selected_song = st.selectbox(
#     "Type or select a song from the dropdown",
#     music_list
# )

# if st.button('Show Recommendation',key='recommendation-button'):
#     recommended_music_names, recommended_music_posters = recommend(selected_song)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommended_music_names[0])
#         st.image(recommended_music_posters[0])
#     with col2:
#         st.text(recommended_music_names[1])
#         st.image(recommended_music_posters[1])

#     with col3:
#         st.text(recommended_music_names[2])
#         st.image(recommended_music_posters[2])
#     with col4:
#         st.text(recommended_music_names[3])
#         st.image(recommended_music_posters[3])
#     with col5:
#         st.text(recommended_music_names[4])
#         st.image(recommended_music_posters[4])

