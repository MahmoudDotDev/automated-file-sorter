
# Automated File Sorter

A simple file sorter for messy directories. Saves time and lives. Sorted by accident? Don't worry, you can undo it!

Automatically organize files by **extension** or **date**, with an easy-to-use graphical interface.

## Features

* 📁 Sort files by extension
* 📅 Sort files by date
* ↩️ Undo previous sorting operations
* 🖥️ Simple graphical interface
* 📝 Keeps a log of file operations
* 🧪 Automated tests
* 📦 No Python installation required when using the AppImage

## Installation

### Linux

#### 1. Clone the repository

```bash
git clone https://github.com/MahmoudDotDev/automated-file-sorter.git
cd automated-file-sorter
```

#### 2. Run the installer

```bash
chmod +x install.sh
./install.sh
```

The installer will:

* Install the application
* Install the application icon
* Create a desktop entry
* Add **Automated File Sorter** to your Applications menu

After installation, you can launch **Automated File Sorter** from your Applications menu.

## Running Without Installing

You can also run the AppImage directly:

```bash
chmod +x Automated_File_Sorter-x86_64.AppImage
./Automated_File_Sorter-x86_64.AppImage
```

## Uninstall

To remove the installed application:

```bash
rm -rf ~/.local/opt/automated-file-sorter
rm -f ~/.local/share/applications/automated-file-sorter.desktop
rm -f ~/.local/share/icons/hicolor/512x512/apps/automated-file-sorter.png
```

## Project Structure

```text
automated-file-sorter/
├── assets/                    # Application assets
├── core/                      # File sorting and undo logic
├── tests/                     # Automated tests
├── gui.py                    # Graphical interface
├── main.py                   # CLI entry point
├── install.sh                # Linux installer
├── build_app.sh              # AppImage build script
├── AutomatedFileSorter.spec  # PyInstaller configuration
└── README.md
```

## Development

If you want to run the project from source instead of using the AppImage:

### Requirements

* Python 3.10+
* Tkinter
* Git

### Setup

```bash
git clone https://github.com/MahmoudDotDev/automated-file-sorter.git
cd automated-file-sorter

python3 -m venv .venv
source .venv/bin/activate
```

Run the GUI:

```bash
python3 gui.py
```

Run the tests:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

