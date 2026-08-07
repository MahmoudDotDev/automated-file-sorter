import os 
import shutil
import json

def undo(log_file="log.json"):
    with open(log_file, "r") as f:
        moves = json.load(f)   

    for move in reversed(moves):
           try:
              shutil.move(move["destination"], move["source"])
           except FileNotFoundError:
               print(f"Skipping missing file: {move['destination']}")
           except Exception as e:
               print(f"Error reverting file: {e}")

