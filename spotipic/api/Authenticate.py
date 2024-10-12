import spotipy
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyOAuth

# Authenticate Spotify API Connection
def get_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="ee0276b06af14ed0b6d37d6b09b82957",
                                               client_secret="1bb2f35b7b05486cabd9dd4baf85743b",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))
    
    return sp

# Authenticate Database Connection to Spotify Songs dataset. From https://www.mongodb.com/resources/languages/python#querying-in-python
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://dbUser:databasepassword@spotipic.fmibk.mongodb.net/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['Spotify_Songs']
  