import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ee0276b06af14ed0b6d37d6b09b82957",
                                               client_secret="1bb2f35b7b05486cabd9dd4baf85743b",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))

print(sp.audio_features('https://open.spotify.com/track/1YFoeeHQ7YIWqAqWbJoJLO?si=f9946c5a12e3476f'))