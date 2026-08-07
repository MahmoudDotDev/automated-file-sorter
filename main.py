from core.sorter import sort_files
from core.logger import save_log
from core.undo import undo 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--mode", choices = ["ext", "date", "all"], required = True)

parser.add_argument("--dry_run", action = "store_true")

parser.add_argument("--verbose", action = "store_true")

args = parser.parse_args()

group = parser.add_mutually_exclusive_group(required = True)

group.add_argument("--undo", help="Undo using log file")
group.add_argument("--path", help="Path to sort")
def main():
    if args.undo:
        undo(args.undo)
        return

    moves = sort_files(
            args.path, 
            args.mode, 
            args.dry_run, 
            args.verbose
        )    
    
    if not args.dry_run and moves:
        save_log(moves)

if __name__ == "__main__":
    main()
