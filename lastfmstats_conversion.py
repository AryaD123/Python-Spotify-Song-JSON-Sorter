"""
File: lastfmstatsconversion.py
Author: Arya Das
Email: adasnxt@gmail.com
Created: 3/8/22
Updated: 3/8/2022
Description:
"""
import datetime
import time
import json

STOP_COMMANDS = ["STOP", "Stop", "stop", "END", "End", "end", "EXIT", "Exit", "exit", "Quit", "quit"]

user_input_file = input("Enter name of a file: ")
song_count = 0
terminate_program = False

try:
    with open(user_input_file) as f:
        json_data = json.load(f)
        print("File was loaded.")
except:
    print("That file does not exist.")
    terminate_program = True

userDateTime = "2017-05-23T02:11:26Z" # Example of spotify date/time format

def convertDateToEpoch(exampleDateTime):
    splitDateTime = exampleDateTime.split("T") # Splits on the letter 'T', creates a list
    dateOnly = splitDateTime[0]
    timeOnly = splitDateTime[1].split("Z")
    splitDate = dateOnly.split("-")
    splitTime = timeOnly[0].split(":")
    # print("Split Date:", splitDate) # Can use for testing
    # print("Split Time:", splitTime) # Can use for testing

    year = int(splitDate[0])
    month = int(splitDate[1])
    dayOfMonth = int(splitDate[2])

    hour = int(splitTime[0])
    minute = int(splitTime[1])
    second = int(splitTime[2])

    # assigned regular string date
    date_time = datetime.datetime(year, month, dayOfMonth, hour, minute, second)

    # print regular python date&time
    # print("date_time =>", date_time) # Can use for testing

    # displaying unix timestamp after conversion
    # print("unix_timestamp => ", (time.mktime(date_time.timetuple()))) # Can use for testing
    return int((time.mktime(date_time.timetuple())))

# convertDateToEpoch(userDateTime)

last_FM_Username = input("Enter your last.fm username: ")
lastFMdict = {"usernme": last_FM_Username, "scrobbles": []}

for iter in json_data:
    trackTimestamp = convertDateToEpoch(iter["ts"])
    lastFMdict["scrobbles"].append({"track": iter["master_metadata_track_name"], "artist": iter["master_metadata_album_artist_name"], "album": iter["master_metadata_track_name"], "date": trackTimestamp})

userExportFile = input("Enter a json file name for exporting data: ")
with open(userExportFile, "w") as exportFile:
    json.dump(lastFMdict, exportFile)

