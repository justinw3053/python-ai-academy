#!/bin/bash
set -e

echo "Building Space Station Academy .deb..."

# Create package structure
BUILD_DIR="build/space-station-academy_1.0-1_amd64"
mkdir -p "$BUILD_DIR/opt/space-station-academy"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/DEBIAN"

# Copy source code (excluding tests and venv)
cp -r backend frontend content scripts "$BUILD_DIR/opt/space-station-academy/"
cp app.py "$BUILD_DIR/opt/space-station-academy/"

# Create desktop shortcut
cat << 'DESKTOP' > "$BUILD_DIR/usr/share/applications/space-station-academy.desktop"
[Desktop Entry]
Name=Aether Station Override Terminal
Comment=Space Station Academy
Exec=/opt/space-station-academy/launch.sh
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Education;Development;
DESKTOP

# Create launcher script
cat << 'LAUNCHER' > "$BUILD_DIR/opt/space-station-academy/launch.sh"
#!/bin/bash
cd /opt/space-station-academy
# Assumes system python3 and deps are installed via depends
python3 app.py
LAUNCHER
chmod +x "$BUILD_DIR/opt/space-station-academy/launch.sh"

# Create debian control file
cat << 'CONTROL' > "$BUILD_DIR/DEBIAN/control"
Package: space-station-academy
Version: 1.0-1
Section: education
Priority: optional
Architecture: amd64
Depends: python3, python3-flask, python3-webview, python3-requests
Maintainer: Justin
Description: Space Station Academy
 An immersive Python and AI curriculum application.
CONTROL

# Build the deb
# dpkg-deb --build "$BUILD_DIR"
echo "Build structure created successfully in build/"
