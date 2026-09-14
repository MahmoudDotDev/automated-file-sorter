import os
import shutil
import json

def undo(log_file="log.json"):
    with open(log_file, "r") as f:
        log_data = json.load(f)

    moves = log_data["moves"]
    created_folders = log_data["created_folders"]

    for move in reversed(moves):
        destination = move["destination"]
        source = move["source"]

        try:
            shutil.move(destination, source)
        except FileNotFoundError:
            print(f"Skipping missing file: {destination}")
        except Exception as e:
            print(f"Error reverting file: {e}")

    for folder in reversed(created_folders):
        try:
            os.rmdir(folder)
            print(f"Removed empty folder: {folder}")
        except OSError:
            pass
