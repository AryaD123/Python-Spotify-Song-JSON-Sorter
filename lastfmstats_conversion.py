"""
File: lastfmstatsconversion.py
Author: Arya Das
Email: adasnxt@gmail.com
Created: 3/8/22
Updated: 3/8/2022
Description:
"""

import json

STOP_COMMANDS = ["STOP", "Stop", "stop", "END", "End", "end", "EXIT", "Exit", "exit", "Quit", "quit"]

user_input_file = input("Enter name of a file: ")
song_count = 0
terminate_program = False

try:
    with open(user_input_file) as f:
        json_data = json.load(f)
except:
    print("That file does not exist.")
    terminate_program = True