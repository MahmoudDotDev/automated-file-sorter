import os
import shutil
import json

def undo(log_file="log.json"):
    with open(log_file, "r") as f:
        moves = json.load(f)

    folders = set()

    for move in reversed(moves):
        destination = move["destination"]
        source = move["source"]

        folders.add(os.path.dirname(destination))

        try:
            shutil.move(destination, source)
        except FileNotFoundError:
            print(f"Skipping missing file: {destination}")
        except Exception as e:
            print(f"Error reverting file: {e}")

    for folder in folders:
        try:
            os.rmdir(folder)
            print(f"Removed empty folder: {folder}")
        except OSError:
            # Folder isn't empty, so leave it alone
            pass
