import sys
import json
import numpy as np
import Authenticate
from Image2Data import photo2features
# from tabulate import tabulate

# Import image path from API Call
image_path = sys.argv[1]
#image_path = './uploads/PatriotHacks-max.jpg'

# Helper function to help format table
# def format_table():
#     output_table = np.empty((7, 2), dtype=object)
#     output_table[0,0] = "Song"
#     output_table[1,0] = "Artist"
#     output_table[2,0] = "Accuracy"
#     output_table[3,0] = "Link"
#     output_table[4,0] = "Image Features"
#     output_table[5,0] = "Song Features"
#     output_table[6,0] = "Color Features"

#     return output_table

# Function that turns image feature data into Spotify data
def features2spotify(path_to_image, num_songs):
    # Turn image into data
    # Outputs [Acousticness, Danceability, Energy, Instrumentalness, and Valence]
    img_features, color_features = photo2features(path_to_image)

    # Connect to Spotify. Used in case you need to do a search for album cover, excetra
    spotify = Authenticate.get_spotify()
    # print("Spotify Connected!")

    # Connect to Database, look at the audio_features collection
    database = Authenticate.get_database()
    # print("Database Connected!")
    song_collection = database['audio_features']

    # Make for loop that checks every songs features and checks error for the features we want
    # Smallest average sum of erros is the selected song

    # This function is looped for number of songs you need, and we skip songs we already have  
    # printout = None 
    # np.set_printoptions(threshold=sys.maxsize)

    id_list = np.empty((num_songs), dtype=object) 
    output_arr = []
    for i in range(num_songs):
        # printout = format_table()
        min_err = sys.float_info.max
        song_name = None
        song_artist = None
        song_id = None
        song_photo = None
        final_features = np.zeros_like(img_features)
        song_details = song_collection.find()
        for song in song_details:
            
            song_features = np.array([song['acousticness'], song['danceability'], song['energy'], song['instrumentalness'], song['valence']])
            error = np.sum(np.abs(np.divide(np.subtract(song_features, img_features), img_features))) * (100 / len(song_features))
    
            if error < min_err and not (f'{song['track_id']}' in id_list):
                min_err = error
                song_name = song['track_name']
                # Try except because datasets naming conventions are different for artist name
                try:
                    song_artist = song['artists']
                except:
                    song_artist = song['artist_name']
                
                song_id = song['track_id']

                song_photo = spotify.track(song_id)['album']['images'][0]['url']
                
                #final_features = song_features

        # For every song, fill table with its relavant data
        id_list[i] = song_id
        # printout[0, 1] = song_name
        # printout[1, 1] = song_artist
        # printout[2, 1] = f"{100-min_err}"
        # printout[3, 1] = f"http://open.spotify.com/track/{song_id}"
        # printout[4, 1] = np.array2string(img_features)
        # printout[5, 1] = np.array2string(final_features)
        # printout[6, 1] = np.array2string(color_features)
        # print(tabulate(printout, tablefmt="fancy_grid"))

        dict = {
            "track_name": song_name,
            "artist": song_artist,
            "album_image": song_photo,
            "spotify_link": "http://open.spotify.com/track/" + str(song_id) 
        }

        output_arr.append(dict)

        # output_arr.append('"artist": "' + song_artist + '"')
        # output_arr.append('"album_image": "' + song_photo + '"')
        # output_arr.append('"spotify_link": "' + f"http://open.spotify.com/track/{song_id}" + '"},')
    

    #print(output_arr)
    # output_arr = '[{}]'.format(', '.join(output_arr)) #https://stackoverflow.com/questions/63088929/how-to-remove-apostrophes-from-a-list-in-python
    # output_arr = output_arr[:-1]

    json_format = json.dumps(output_arr, indent=2)
    print(json_format)
    database.client.close()
        
features2spotify(image_path, 5)