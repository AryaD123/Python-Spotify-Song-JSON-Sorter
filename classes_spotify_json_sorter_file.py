"""
File: classes_spotify_json_sorter_file.py
Author: Arya Das
Email: adasnxt@gmail.com
Created: 6/15/2021
Updated: 6/16/2021
Description: last.fm similar function for spotify json files, using classes
Extra Notes: None
"""
import json

STOP_COMMANDS = ["STOP", "Stop", "stop", "END", "End", "end", "EXIT", "Exit", "exit", "Quit", "quit"]
user_input_file = input("Enter name of a file: ")
song_count = 0
# artist_dict = {}

with open(user_input_file) as f:
    json_data = json.load(f)


class Artist:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.artist_songs = {}
        self.artist_albums = {}
        self.artist_total_plays = 0
        self.time_played = 0


class Podcast:
    def __init__(self, podcast_name):
        self.podcast_name = podcast_name
        self.time_played = 0
        self.episodes = {}
        self.total_plays = 0


user_input_choice = input("Enter '1' to view music Stats, Enter '2' to view podcast stats: ")


# user_input_artist = input("Enter an artist name: ")
# user_artist = Artist(user_input_artist)

def check_data():
    if user_input_choice == "1":
        user_input_artist = input("Enter an artist name: ")
        user_artist = Artist(user_input_artist)
        print("Running...")
        index_count = 1
        for i in json_data:
            if index_count < 8049:
                # Only for Arya's Data
                # Used to ignore songs already scrobbled through Last.FM to avoid repeat data
                if i['master_metadata_album_artist_name'] == user_input_artist:
                    if i["master_metadata_track_name"] in user_artist.artist_songs:
                        user_artist.artist_songs[i["master_metadata_track_name"]] += 1
                    else:
                        user_artist.artist_songs[i["master_metadata_track_name"]] = 1

                    if i["master_metadata_album_album_name"] in user_artist.artist_albums:
                        user_artist.artist_albums[i["master_metadata_album_album_name"]] += 1
                    else:
                        user_artist.artist_albums[i["master_metadata_album_album_name"]] = 1

                    user_artist.artist_total_plays += 1
                    user_artist.time_played += i["ms_played"]
            index_count += 1

        print("Artist:", user_artist.artist_name)
        print("Artist Songs:", user_artist.artist_songs)
        print("Artist Albums:", user_artist.artist_albums)
        print("Artist Total Plays:", user_artist.artist_total_plays)
        print("Artist Time Played (milliseconds):", user_artist.time_played)
        print("Artist Time Played (minutes):", ((user_artist.time_played / 1000) / 60))
        print(" ")

    elif user_input_choice == "2":
        user_input_podcast = input("Enter a podcast name: ")
        user_podcast = Podcast(user_input_podcast)
        print("Running...")
        for j in json_data:
            if j["episode_show_name"] == user_input_podcast:
                user_podcast.total_plays += 1

                if j["episode_name"] in user_podcast.episodes:
                    user_podcast.episodes[j["episode_name"]] += 1
                else:
                    user_podcast.episodes[j["episode_name"]] = 1

                user_podcast.time_played += j["ms_played"]

        print("Podcast Name:", user_podcast.podcast_name)
        print("Podcast Episodes:", user_podcast.episodes)
        print("Podcast Total Plays:", user_podcast.total_plays)
        print("Podcast Total Time Played (Milliseconds):", user_podcast.time_played)
        print("Podcast Total Time Played (Minutes):", ((user_podcast.time_played / 1000) / 60))
        print(" ")

    else:
        print("Please type in '1' or '2'.")


while user_input_choice not in STOP_COMMANDS:
    check_data()
    # user_input_artist = input("Enter an artist name: ")
    user_input_choice = input("Enter '1' to view music Stats, Enter '2' to view podcast stats: ")
print("Ending Program...")
print("Thanks for using!")
