#!/usr/bin/env bash
set -euo pipefail

echo "Installing Solar Neo v0.7 — PROJECT: SOLAR"

# Determine absolute path of script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

DEST_SHARE="$HOME/.local/share/solar-neo"
DEST_BIN="$HOME/.local/bin"

mkdir -p "$DEST_SHARE" "$DEST_BIN"

# Copy solarneo client folder
if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$SCRIPT_DIR/solarneo" "$DEST_SHARE/"
else
    cp -r "$SCRIPT_DIR/solarneo" "$DEST_SHARE/"
fi

# Install wrappers — they'll always call python -m
cat > "$DEST_BIN/solar" <<EOF
#!/usr/bin/env bash
python3 -m solarneo "\$@"
EOF

cat > "$DEST_BIN/sln" <<EOF
#!/usr/bin/env bash
python3 -m solarneo "\$@"
EOF

chmod +x "$DEST_BIN/solar" "$DEST_BIN/sln"

echo "✅ Installed Solar Neo to:"
echo "  - $DEST_SHARE (core)"
echo "  - $DEST_BIN (commands)"

# PATH advisory
if [[ ":$PATH:" != *":$DEST_BIN:"* ]]; then
    echo "⚠️  $DEST_BIN is not in your PATH."
    echo "   Add it with:"
    echo "   echo 'export PATH=\"\$PATH:$DEST_BIN\"' >> ~/.bashrc"
else
    echo "✔ $DEST_BIN found in PATH"
fi

echo "Try:"
echo "  solar sys"
echo "  solar version"
