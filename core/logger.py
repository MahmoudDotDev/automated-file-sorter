import json

def save_log(moves, log_file="log.json"):
    with open(log_file, "w") as f:
        json.dump(moves, f, indent = 4)

def load_log(log_file="log.json"):
    with open(log_file, "r") as f:
         return json.load(f)

def cli_logger(msg):
    print(msg)

def gui_logger(text_widget):
    def log(msg):
        text_widget.insert("end", msg + "\n")
        text_widget.see("end")
    return log
