#!/bin/bash

set -e

APP_NAME="AutomatedFileSorter"
APPIMAGE_NAME="Automated_File_Sorter-x86_64.AppImage"

echo "========================================"
echo " Building Automated File Sorter"
echo "========================================"

echo
echo "[1/5] Cleaning previous builds..."

rm -rf build dist
rm -f "$APPIMAGE_NAME"

echo
echo "[2/5] Building PyInstaller executable..."

pyinstaller --onefile --windowed \
	--name "$APP_NAME" \
	gui.py

echo
echo "[3/5] Preparing AppDir..."

mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/512x512/apps

cp "dist/$APP_NAME" "AppDir/usr/bin/$APP_NAME"

cp assets/icon.png \
	AppDir/usr/share/icons/hicolor/512x512/apps/automated-file-sorter.png

cp AppDir/usr/share/applications/automated-file-sorter.desktop \
	AppDir/

cp assets/icon.png \
	AppDir/automated-file-sorter.png

chmod +x AppDir/AppRun

echo
echo "[4/5] Building AppImage..."

ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir

echo
echo "[5/5] Build complete!"
echo
echo "Output:"
ls -lh "$APPIMAGE_NAME"

echo
echo "Run it with:"
echo "./$APPIMAGE_NAME"
echo
