"""
File: classes_spotify_sorter_v3.py
Author: Arya Das
Email: adasnxt@gmail.com
Created: 12/19/2021
Updated: 1/13/2022
Description:
- similar to Version 2, looking to add data fields for play dates/times
- looking to be able to pull from multiple json files (presumably for different spotify/last.fm users and do a comparison
Extra Notes:
- 8049 is Last.fm cutoff for Arya's Spotify data
"""
import json
import operator

STOP_COMMANDS = ["STOP", "Stop", "stop", "END", "End", "end", "EXIT", "Exit", "exit", "Quit", "quit"]
PRESET_FILE_NAMES = ["python_sorted_endsong_0.json"]

def determine_file():
    file_input_choice = input("Enter 1 to choose preset files or 2 to enter your own file name: ")
    while (file_input_choice != "1") and (file_input_choice != "2"):
        file_input_choice = input("Please enter 1 to choose preset files or 2 to enter your own file name: ")

    if file_input_choice == "1":
        file_name_counter = 1
        for i in PRESET_FILE_NAMES:
            print("File", str(file_name_counter) + ")", i)
        user_input_file = int(input("Enter number of file: "))
        while user_input_file > len(PRESET_FILE_NAMES):
            user_input_file = int(input("Please enter number of file: "))


user_input_file = input("Enter name of a file: ")
song_count = 0
terminate_program = False

try:
    with open(user_input_file) as f:
        json_data = json.load(f)
except:
    print("That file does not exist.")
    terminate_program = True

class Artist:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.artist_songs = {}
        self.artist_albums = {}
        self.artist_total_plays = 0
        self.time_played = 0
        self.timestamps = []
        self.type = "Artist"

class Podcast:
    def __init__(self, podcast_name):
        self.podcast_name = podcast_name
        self.time_played = 0
        self.episodes = {}
        self.total_plays = 0
        self.timestamps = []
        self.type = "Podcast"

# think about how to implement stats for day, month, year, unique listens, etc
class Date:
    def __init__(self, year):
        self.year = year
        self.month = ""
        self.day = ""
        self.daily_plays = 0
        self.time_played = 0

if terminate_program == False:
    user_input_choice = input("Enter '1' to view music Stats, Enter '2' to view podcast stats: ")
else:
    user_input_choice = STOP_COMMANDS[0]

def sort(param_class_and_key):
    # meant to sort ANY class object when called, regardless of music or podcast
    sort_list = []
    counter = 10000
    while counter > 0:
        for i in param_class_and_key:
            if param_class_and_key[i] >= counter and i not in sort_list and {i: param_class_and_key[i]} not in sort_list:
                sort_list.append({i: param_class_and_key[i]})
        counter -= 1

    return sort_list

def display_artist(param_class):
    print("Artist:", param_class.artist_name)
    # print("Artist Songs:", param_class.artist_songs)
    print("Artist Songs:")

    sorted_artist_songs = sort(param_class.artist_songs)
    for sort_song_iter in sorted_artist_songs:
        print("\t" + str(sort_song_iter))

    print("Artist Albums:")

    sorted_artist_albums = sort(param_class.artist_albums)
    for sort_album_iter in sorted_artist_albums:
        print("\t" + str(sort_album_iter))

    print("Artist Total Plays:", param_class.artist_total_plays)
    print("Artist Time Played (milliseconds):", param_class.time_played)
    print("Artist Time Played (minutes):", ((param_class.time_played / 1000) / 60))
    if len(param_class.timestamps) > 0:
        print("First Played:", param_class.timestamps[0])
        print("Last Played:", param_class.timestamps[-1])
    print(" ")

def display_podcast(param_class):
    print("Podcast Name:", param_class.podcast_name)
    # print("Podcast Episodes:", param_class.episodes)
    print("Podcast Episodes:")

    sorted_podcast_songs = sort(param_class.episodes)
    for sort_episodes_iter in sorted_podcast_songs:
        print("\t" + str(sort_episodes_iter))

    print("Podcast Total Plays:", param_class.total_plays)
    print("Podcast Total Time Played (Milliseconds):", param_class.time_played)
    print("Podcast Total Time Played (Minutes):", ((param_class.time_played / 1000) / 60))
    if len(param_class.timestamps) > 0:
        print("First Played:", param_class.timestamps[0])
        print("Last Played:", param_class.timestamps[-1])
    print(" ")

def determine_cutoff():
    user_input_cutoff = input("Enter 'A' to stop stat tracking at a certain index, enter 'B' to track complete stats: ")

    if user_input_cutoff.upper() != "A" and user_input_cutoff.upper() != "B":
        while user_input_cutoff.upper() != "A" and user_input_cutoff.upper() != "B":
            print("Error, select 'A' or 'B'")
            user_input_cutoff = input(
                "Enter 'A' to stop stat tracking at a certain index, enter 'B' to track complete stats (If unsure, select 'B'): ")
    if user_input_cutoff.upper() == "A":
        user_cutoff_num = input("Enter an index to stop at: ")
        # while user_cutoff_num not in range(0, len(json_data)):
        try:
            user_cutoff_num = int(user_cutoff_num)
        except:
            if user_input_cutoff not in range(0, len(json_data)):
                while user_cutoff_num not in range(0, len(json_data)):
                    user_cutoff_num = input("Error, please enter an index number between 0 and " + str(len(json_data)) + ": ")
                    try:
                        user_cutoff_num = int(user_cutoff_num)
                    except:
                        user_cutoff_num = input("Error, please enter an index NUMBER between 0 and " + str(len(json_data)) + ": ")

    elif user_input_cutoff.upper() == "B":
        print("Calculating stats based on all data in file.")
        user_cutoff_num = len(json_data)
    return user_cutoff_num

def check_data():
    if user_input_choice == "1" or user_input_choice == "2":
        # implement a condition in which user gets asked if they want to keep same cutoff or not
        chosen_cutoff = determine_cutoff()
    if user_input_choice == "1":
        user_input_artist = input("Enter an artist name: ")
        user_artist = Artist(user_input_artist)
        print("Running...")
        index_count = 1
        for i in json_data:
            if index_count < int(chosen_cutoff):
                # 8049 is Last.fm cutoff for Arya's Spotify data
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
                    user_artist.timestamps.append(i["ts"])


            index_count += 1

        display_artist(user_artist)

    elif user_input_choice == "2":
        user_input_podcast = input("Enter a podcast name: ")
        user_podcast = Podcast(user_input_podcast)
        print("Running...")
        index_count = 1
        for j in json_data:
            if index_count < int(chosen_cutoff):
                if j["episode_show_name"] == user_input_podcast:
                    user_podcast.total_plays += 1

                    if j["episode_name"] in user_podcast.episodes:
                        user_podcast.episodes[j["episode_name"]] += 1
                    else:
                        user_podcast.episodes[j["episode_name"]] = 1

                    user_podcast.time_played += j["ms_played"]
                    user_podcast.timestamps.append(j["ts"])
            index_count += 1

        display_podcast(user_podcast)

    elif user_input_choice != "1" and user_input_choice != "2":
        print("Please type in '1' or '2'.")

while user_input_choice not in STOP_COMMANDS:
    check_data()
    user_input_choice = input("Enter '1' to view music Stats, Enter '2' to view podcast stats: ")
print("Ending Program...")
print("Thanks for using!")
