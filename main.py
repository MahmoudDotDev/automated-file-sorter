import os
import shutil

folder = "/home/mahmoud/Github/Personal/automated-file-sorter/test_folder/"


def list_files():
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
    full_path = os.path.join(folder, file_name)
    folder_created = os.makedirs(full_path, exist_ok = True)
    source = os.path.join(folder, file)
    destination = os.path.join(full_path, file)
    shutil.move(source, destination)
    print(f"Folder {file_name} made.")

def file_sorter(file_ext):
    file_ext = os.path.splitext(file)[1]
    file_name = os.path.splitext(file)[1]
    shutil.move(source, destination)

def main():
    
    for file in os.listdir(folder):
        folder_generator(file)



if __name__ == "__main__":
    main()
