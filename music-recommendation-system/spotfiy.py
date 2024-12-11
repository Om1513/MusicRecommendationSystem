import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os


dotenv.load_dotenv()

# Debugging: Print loaded environment variables
print("Client ID:", os.getenv('SPOTIPY_CLIENT_ID'))
print("Client Secret:", os.getenv('SPOTIPY_CLIENT_SECRET'))
print("Redirect URI:", os.getenv('SPOTIPY_REDIRECT_URI'))

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri,scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None