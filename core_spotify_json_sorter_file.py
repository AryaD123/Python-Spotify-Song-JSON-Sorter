"""
File: core_spotify_json_sorter_file.py
Author: Arya Das
Email: adasnxt@gmail.com
Created: 6/15/2021
Updated: 6/16/2021
Description: last.fm similar function for spotify json files
Extra Notes: None
"""
import json
# import csv

user_input_file = input("Enter name of a file: ")
index_count = 0
song_count = 0
artist_dict = {}


with open(user_input_file) as f:
    json_data = json.load(f)

while index_count < 8049:
    for i in json_data:
        if index_count < 8049:
            if i['master_metadata_album_artist_name'] != "null" or i['master_metadata_album_artist_name'] != "none":
                song_count += 1
                if i['master_metadata_album_artist_name'] not in artist_dict:
                    artist_dict[i['master_metadata_album_artist_name']] = {"Artist": i['master_metadata_album_artist_name'], "Amount": 1, "Total Time Played": i['ms_played']}
                else:
                    artist_dict[i['master_metadata_album_artist_name']]["Amount"] += 1
                    artist_dict[i['master_metadata_album_artist_name']]["Total Time Played"] += i['ms_played']
        print(index_count, i)
        index_count += 1
    print(" ")

for j in artist_dict:
    print(artist_dict[j])
    # print(" ")

print(song_count)
