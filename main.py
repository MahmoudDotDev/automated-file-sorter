from core.sorter import sort_files
from core.logger import save_log
from core.undo import undo 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--mode", choices = ["ext", "date", "all"], required = True, help = "Gives the option to choose by what criteria are the file gonna be sorted")

parser.add_argument("--dry_run", action = "store_true", help = "Shows what the output would be without running the program")

parser.add_argument("--verbose", action = "store_true", help = "Gives more detailed logs")

group = parser.add_mutually_exclusive_group(required = True)

group.add_argument("--undo", help="Undo using log file")
group.add_argument("--path", help="Path to sort")

args = parser.parse_args()

def main():
    if args.undo:
        undo(args.undo)
        return

    moves, created_folders, count= sort_files(
            args.path, 
            args.mode, 
            args.dry_run, 
            args.verbose
        )    
    
    if not args.dry_run and moves:
        save_log(moves, created_folders)

if __name__ == "__main__":
    main()
