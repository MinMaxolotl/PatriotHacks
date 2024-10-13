import spotipy
import certifi
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyOAuth

#Authenticate Spotify API Connection
def get_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="b9dfd388174f49a6af045a4c3d9ef63b",
                                               client_secret="efb1951db23444e2a4706434e329f75a",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))

    return sp

#Authenticate Database Connection to Spotify Songs dataset. From https://www.mongodb.com/resources/languages/python#querying-in-python
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://dbUser:databasepassword@spotipic.fmibk.mongodb.net/"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING, maxPoolSize=10, maxIdleTimeMS=60000, tlsCAFile=certifi.where())
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['Spotify_Songs']