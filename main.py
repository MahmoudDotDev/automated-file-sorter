import os
import shutil
import datetime

folder = "/home/mahmoud/Github/Personal/automated-file-sorter/test_folder/"

def list_files():
    for i, file in enumerate(files):
        print(f"{i}. {file}")
        
def file_definer(file):
    file_name = os.path.splitext(file)[0]
    file_ext = os.path.splitext(file)[1]
    print(file_ext)

def folder_generator(file):
    if not os.path.isfile(os.path.join(folder, file)):w:
        return
    
    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:] #Removes the dot in ".txt"
    full_path = os.path.join(folder, file_name)
    folder_created = os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(full_path, file)
    shutil.move(source, destination)
    print(f"Folder {file_name} made.")

def folder_generator_time(file):
    print("Checking:", file)
    if not os.path.isfile(os.path.join(folder, file)):
       return
    time_stamp = os.path.getmtime(os.path.join(folder, file))
    date = datetime.datetime.fromtimestamp(time_stamp)
    folder_name = f"{date.year}-0{date.month}"
    full_path = os.path.join(folder, folder_name)
    folder_created = os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(folder, folder_name, file)
    shutil.move(source, destination)
    print(f"Moved {file} -> {folder_name}")

def folder_generator_all(file):
    if not os.path.isfile(os.path.join(folder, file)):
       return
    time_stamp = os.path.getmtime(os.path.join(folder, file))
    date = datetime.datetime.fromtimestamp(time_stamp)
    folder_name = f"{date.year}-0{date.month}"
    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:]
    full_path = os.path.join(folder, file_name)
    date_folder = os.makedirs(full_path, exist_ok = True)
    ext_folder = os.makedirs(os.path.join(full_path, date_folder), exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(folder, folder_name, file_name, file)
    shutil.move(source, destination)
    print(f"Moved {file} -> {folder_name}")
    

def main():
    choice = input("File Sorting options (ext or date or dext) : ")
    
    if choice == "ext":
        for file in os.listdir(folder):
            folder_generator(file)

    elif choice == "date":
        for file in os.listdir(folder):
            folder_generator_time(file)
    
    elif choice == "dext":
         for file in os.listdir(folder):
             folder_generator_all(file)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
