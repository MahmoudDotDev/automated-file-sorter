#!/bin/bash

set -e

APP_NAME="Automated File Sorter"
APP_ID="automated-file-sorter"
INSTALL_DIR="$HOME/.local/opt/$APP_ID"
APPLICATIONS_DIR="$HOME/.local/share/applications"
ICONS_DIR="$HOME/.local/share/icons/hicolor/512x512/apps"

APPIMAGE="Automated_File_Sorter-x86_64.AppImage"
ICON="assets/icon.png"

echo "========================================"
echo " Installing $APP_NAME"
echo "========================================"

if [ ! -f "$APPIMAGE" ]; then
	echo "Error: $APPIMAGE was not found."
	echo "Make sure the AppImage is in the project directory."
	exit 1
fi

if [ ! -f "$ICON" ]; then
	echo "Error: $ICON was not found."
	exit 1
fi

echo
echo "[1/4] Creating installation directories..."

mkdir -p "$INSTALL_DIR"
mkdir -p "$APPLICATIONS_DIR"
mkdir -p "$ICONS_DIR"

echo
echo "[2/4] Installing application..."

cp "$APPIMAGE" "$INSTALL_DIR/$APPIMAGE"
chmod +x "$INSTALL_DIR/$APPIMAGE"

echo
echo "[3/4] Installing icon..."

cp "$ICON" "$ICONS_DIR/$APP_ID.png"

echo
echo "[4/4] Creating desktop entry..."

cat >"$APPLICATIONS_DIR/$APP_ID.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Comment=Automatically organize files by extension and date
Exec=$INSTALL_DIR/$APPIMAGE
Icon=$APP_ID
Terminal=false
Categories=Utility;
Keywords=file;organizer;sorter;files;
EOF

chmod +x "$APPLICATIONS_DIR/$APP_ID.desktop"

echo
echo "========================================"
echo " Installation complete!"
echo "========================================"
echo
echo "$APP_NAME is now available in your"
echo "Applications menu."
echo
echo "You can search for:"
echo "  $APP_NAME"
echo
