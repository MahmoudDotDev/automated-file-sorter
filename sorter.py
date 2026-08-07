import os 
import argparse
import shutil
import datetime 

parser = argparse.ArgumentParser()

parser.add_argument("--path", required = True)

parser.add_argument("--mode", choices = ["ext", "date", "both"], required = True)

parser.add_argument("--dry-run", action = "store_true")

args = parser.parse_args()

folder = args.path

def list_files(files):
    for i, file in enumerate(files):
        print(f"{i}. {file}")
        
def file_definer(file):
    file_name = os.path.splitext(file)[0]
    file_ext = os.path.splitext(file)[1]
    print(file_ext)

def folder_generator(file):
    if not os.path.isfile(os.path.join(folder, file)):
        return

    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:] #Removes the dot in ".txt"
    folder_name = file_name
    full_path = os.path.join(folder, file_name)
    os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(full_path, file)
    move_file(source, destination, file, folder_name, file_name)

def folder_generator_time(file):
    print("Checking:", file)
    if not os.path.isfile(os.path.join(folder, file)):
       return
    time_stamp = os.path.getmtime(os.path.join(folder, file))
    date = datetime.datetime.fromtimestamp(time_stamp)
    folder_name = f"{date.year}-{date.month:02d}"
    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:]    
    full_path = os.path.join(folder, folder_name)
    os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(folder, folder_name, file)
    move_file(source, destination, file, folder_name, file_name)

def folder_generator_all(file):
    if not os.path.isfile(os.path.join(folder, file)):
       return
    time_stamp = os.path.getmtime(os.path.join(folder, file))
    date = datetime.datetime.fromtimestamp(time_stamp)
    folder_name = f"{date.year}-0{date.month:02d}"
    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:]
    date_folder = folder_name
    full_path = os.path.join(folder, file_name, date_folder)
    ext_folder = os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(full_path, file)
    move_file(source, destination, file, folder_name, file_name)
    
def move_file(source, destination, file, folder_name, file_name):
    if args.dry_run:
        print(f"[DRY RUN] {file} -> {file_name}/{folder_name}\n")
    else:
        shutil.move(source, destination)
        print(f"Moved {file} -> {folder_name}/{file_name}")

def main():
    
    if args.mode == "ext":
         for file in os.listdir(folder):
            folder_generator(file)

    elif args.mode == "date":
        for file in os.listdir(folder):
            folder_generator_time(file)

    elif args.mode == "both":
        for file in os.listdir(folder):
            folder_generator_all(file)

if __name__ == "__main__":
    main()
