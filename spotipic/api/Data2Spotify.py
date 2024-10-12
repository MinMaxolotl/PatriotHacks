import spotipy
import sys
import Authenticate
from pymongo import MongoClient
from Image2Data import photo2features

# Import image path from API Call
image_path = sys.argv[1]

# Turn image into data
# Outputs Acousticness, Danceability, Energy, Instrumentalness, and Valence
a,d,e,i,v = photo2features(image_path)

# Connect to Spotify
spotify = Authenticate.get_spotify()
print("Spotify Connected!")

# Connect to Database, look at the audio_features collection
database = Authenticate.get_database()
print("Database Connected!")
song_collection = database['audio_features']

song_details = song_collection.find()
# for song in song_details:
#    print(song['danceability'])