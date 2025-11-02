#!/usr/bin/env bash
set -euo pipefail

# Detect HOME and user safely
HOME_DIR="${HOME:-$(getent passwd "$(id -u)" | cut -d: -f6)}"
BIN_DIR="$HOME_DIR/.local/bin"
CFG_DIR="$HOME_DIR/.config/neo"

echo "[neo] Installing into $BIN_DIR ..."

mkdir -p "$BIN_DIR" "$CFG_DIR" "$HOME_DIR/.local/state/neo"
# copy entrypoint
cp -f neo.sh "$BIN_DIR/neo"
chmod +x "$BIN_DIR/neo"

# copy python package to ~/.local/share/neo/neo
PKG_DIR="$HOME_DIR/.local/share/neo"
mkdir -p "$PKG_DIR"
cp -R neo "$PKG_DIR/neo"

# create default config if missing
CFG_FILE="$CFG_DIR/config.toml"
if [ ! -f "$CFG_FILE" ]; then
  cat > "$CFG_FILE" <<'EOF'
# neo config (TOML)
# You can toggle features here.
color = true
aur_auto_offer = true
EOF
fi

echo "[neo] Installed. Ensure ~/.local/bin is on PATH."
echo "      Add to shell rc if needed: export PATH=\"$HOME/.local/bin:\$PATH\""
echo "Run: neo -h"
