#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PKG_DIR="$SCRIPT_DIR/deb/vc_wifitracker"
OUTPUT_DIR="$SCRIPT_DIR/dist"

# Read version from control file
VERSION=$(grep -m1 '^Version:' "$PKG_DIR/DEBIAN/control" | awk '{print $2}')
PKG_NAME="vc-wifitracker_${VERSION}_all.deb"

echo "==> Building $PKG_NAME"

# Ensure correct permissions on DEBIAN scripts
chmod 755 "$PKG_DIR/DEBIAN/preinst"
chmod 755 "$PKG_DIR/DEBIAN/postinst"
chmod 755 "$PKG_DIR/DEBIAN/prerm"
chmod 755 "$PKG_DIR/DEBIAN/postrm"

# Ensure correct permissions on application files
chmod 750 "$PKG_DIR/opt/vc-wifitracking/app.py"
chmod 700 "$PKG_DIR/opt/vc-wifitracking/wifi_mode_manager.sh"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build the package
dpkg-deb --build "$PKG_DIR" "$OUTPUT_DIR/$PKG_NAME"

echo "==> Package built: $OUTPUT_DIR/$PKG_NAME"
echo "==> Install with: sudo dpkg -i $OUTPUT_DIR/$PKG_NAME"
