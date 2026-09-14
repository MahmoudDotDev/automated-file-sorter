from core.logger import save_log, gui_logger
from core.sorter import sort_files
from core.undo import undo

import tkinter as tk
from tkinter import filedialog, ttk
import threading


class App:
    def __init__(self, root):
        self.root = root

        # --- Window Configuration ---
        self.root.title("Automated File Sorter")
        self.root.geometry("520x420")
        self.root.minsize(520, 420)

        # --- Main Container ---
        main = tk.Frame(root, padx=20, pady=20)
        main.pack(fill="both", expand=True)

        # --- Folder Section ---
        self.path_var = tk.StringVar()

        tk.Label(
            main,
            text="Folder",
            font=("Helvetica", 12)
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        tk.Entry(
            main,
            textvariable=self.path_var,
            width=40
        ).grid(
            row=1,
            column=0,
            padx=(0, 10),
            pady=5,
            sticky="ew"
        )

        tk.Button(
            main,
            text="Browse",
            command=self.browse_folder
        ).grid(
            row=1,
            column=1,
            pady=5
        )

        # --- Mode Section ---
        self.mode_var = tk.StringVar(value="ext")

        tk.Label(
            main,
            text="Mode",
            font=("Helvetica", 12)
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(10, 0)
        )

        mode_frame = tk.Frame(main)
        mode_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w"
        )

        tk.Radiobutton(
            mode_frame,
            text="Ext",
            variable=self.mode_var,
            value="ext"
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            mode_frame,
            text="Date",
            variable=self.mode_var,
            value="date"
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            mode_frame,
            text="All",
            variable=self.mode_var,
            value="all"
        ).pack(side="left", padx=5)

        # --- Options ---
        self.dry_var = tk.BooleanVar(value=False)
        self.verbose_var = tk.BooleanVar(value=False)

        options_frame = tk.Frame(main)
        options_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10,
            sticky="w"
        )

        tk.Checkbutton(
            options_frame,
            text="Dry Run",
            variable=self.dry_var
        ).pack(side="left", padx=10)

        tk.Checkbutton(
            options_frame,
            text="Verbose",
            variable=self.verbose_var
        ).pack(side="left", padx=10)

        # --- Buttons ---
        button_frame = tk.Frame(main)
        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )

        self.sort_button = tk.Button(
            button_frame,
            text="Sort",
            width=12,
            command=self.sort
        )
        self.sort_button.pack(side="left", padx=10)

        self.undo_button = tk.Button(
            button_frame,
            text="Undo",
            width=12,
            command=self.undo
        )
        self.undo_button.pack(side="left", padx=10)

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(
            main,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(5, 0),
            sticky="ew"
        )

        self.progress_label = tk.Label(
            main,
            text="0 / 0"
        )
        self.progress_label.grid(
            row=7,
            column=0,
            columnspan=2
        )

        # --- Output Console ---
        self.output = tk.Text(
            main,
            height=10,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white"
        )
        self.output.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=(10, 0)
        )

        # --- Responsive Layout ---
        main.columnconfigure(0, weight=1)
        main.rowconfigure(8, weight=1)

        # --- Logger ---
        self.logger = gui_logger(self.output)

        # Track whether a sort is currently running.
        self.sorting = False

    # ---------------------------------------------------------
    # Folder Selection
    # ---------------------------------------------------------

    def browse_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.path_var.set(folder)

    # ---------------------------------------------------------
    # Sorting
    # ---------------------------------------------------------

    def sort(self):
        if self.sorting:
            return

        if not self.path_var.get():
            self.logger("Please select a folder first.")
            return

        self.sorting = True

        self.sort_button.config(state="disabled")
        self.undo_button.config(state="disabled")

        self.output.delete("1.0", "end")

        self.progress["value"] = 0
        self.progress_label.config(text="0 / 0")

        self.logger("Starting sorting...")

        thread = threading.Thread(
            target=self.run_sorting,
            daemon=True
        )

        thread.start()

    def run_sorting(self):
        try:
            moves, created_folders, count = sort_files(
                self.path_var.get(),
                self.mode_var.get(),
                self.dry_var.get(),
                self.verbose_var.get(),
                logger=self.thread_safe_logger,
                progress_callback=self.update_progress
            )

            # Save the undo log only when actual changes were made.
            if moves and not self.dry_var.get():
                save_log(moves, created_folders)

            self.root.after(
                0,
                lambda: self.finish_sorting(count)
            )

        except Exception as error:
            self.root.after(
                0,
                lambda: self.handle_error(error)
            )

    def update_progress(self, current, total):
        def update():
            self.progress["maximum"] = total
            self.progress["value"] = current

            percent = (
                int((current / total) * 100)
                if total > 0
                else 0
            )

            self.progress_label.config(
                text=f"{current} / {total} ({percent}%)"
            )

        self.root.after(0, update)

    def thread_safe_logger(self, message):
        self.root.after(
            0,
            lambda: self.logger(message)
        )

    def finish_sorting(self, count):
        self.logger(
            f"Sorting completed. {count} file(s) processed."
        )

        self.sorting = False

        self.sort_button.config(state="normal")
        self.undo_button.config(state="normal")

    def handle_error(self, error):
        self.logger(
            f"Error: {error}"
        )

        self.sorting = False

        self.sort_button.config(state="normal")
        self.undo_button.config(state="normal")

    # ---------------------------------------------------------
    # Undo
    # ---------------------------------------------------------

    def undo(self):
        if self.sorting:
            return

        self.output.delete("1.0", "end")
        self.logger("Starting undo...")

        try:
            undo("log.json")
            self.logger("Undo completed.")

        except FileNotFoundError:
            self.logger("No undo log was found.")

        except Exception as error:
            self.logger(
                f"Undo failed: {error}"
            )


# -------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()

    app = App(root)

    root.mainloop()
