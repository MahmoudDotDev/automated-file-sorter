import os
import shutil 
import datetime

def sort_files(folder, mode, dry, verbose, logger=print, progress_callback=None):
    moves = []
    files = os.listdir(folder)
    total = len([f for f in files if os.path.isfile(os.path.join(folder, f))])
    count = 0

    for file in files:
        full_path = os.path.join(folder, file)

        if not os.path.isfile(full_path):
            continue 
        
        if verbose:
            logger(f"Processing: {file}")
            
        source = full_path
        
        destination, folder_name, file_name = get_destination(file, folder, mode)
        
        if verbose:
            logger(f"Target folder: {folder_name}")

        if destination is None:
            count += 1
            if progress_callback:
                progress_callback(count, total)
            continue  
        
        success, final_destination = move_file(source, destination, file, folder_name, file_name, dry, verbose, logger)  

        if success and not dry:
           moves.append({
               "source": source,
               "destination": final_destination 
               })
  
        count += 1  
        if progress_callback:
            progress_callback(count, total)

    return moves, count 

def move_file(source, destination, file, folder_name, file_name, dry, verbose, logger):
    
    original_destination = destination 
    destination = get_unique_name(destination)
    
    if verbose and destination != original_destination:
        logger(f"Renamed : {os.path.basename(destination)}")
    if dry:
        logger(f"[DRY RUN] {file} -> {os.path.basename(destination)}")
        return True, destination
    try:

        dir_path = os.path.dirname(destination)

        if verbose:
            logger(f"Creating directory: {dir_path}")


        os.makedirs(dir_path, exist_ok=True) 
        shutil.move(source, destination)
        
        logger(f"Moved {file} -> {os.path.basename(destination)}\n")
        return True, destination  
    
    except Exception as e:
        logger(f"Error moving {file} : {e}")
        return False, None

def get_unique_name(destination):
    base, ext = os.path.splitext(destination)
    counter = 1

    new_destination = destination
    
    while os.path.exists(new_destination):
        new_destination = f"{base} ({counter}){ext}"
        counter += 1

    return new_destination 

def get_destination(file, folder, mode):
    file_ext = os.path.splitext(file)[1]
    file_name = file_ext[1:] if file_ext else "no_ext"

    if mode == "ext":
        folder_name = file_name
        full_path = os.path.join(folder, folder_name)

    elif mode == "date":
        time_stamp = os.path.getmtime(os.path.join(folder, file))
        date = datetime.datetime.fromtimestamp(time_stamp)
        folder_name = f"{date.year}-{date.month:02d}"
        full_path = os.path.join(folder, folder_name)

    elif mode == "all":
        time_stamp = os.path.getmtime(os.path.join(folder, file))
        date = datetime.datetime.fromtimestamp(time_stamp)
        folder_name = f"{date.year}-{date.month:02d}"
        full_path = os.path.join(folder, file_name, folder_name)

    else:
        return None, None, None 
    
    destination = os.path.join(full_path, file)

    return destination, folder_name, file_name



