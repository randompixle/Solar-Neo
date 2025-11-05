#!/usr/bin/env bash
set -euo pipefail

echo "Installing Solar Neo v0.7 — PROJECT: SOLAR"

# Determine absolute script location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

DEST_SHARE="$HOME/.local/share/solar-neo"
DEST_BIN="$HOME/.local/bin"

mkdir -p "$DEST_SHARE" "$DEST_BIN"

# Copy solarneo folder to share location
if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$SCRIPT_DIR/solarneo" "$DEST_SHARE/"
else
    cp -r "$SCRIPT_DIR/solarneo" "$DEST_SHARE/"
fi

# Create launcher scripts
cat > "$DEST_BIN/solar" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="\$HOME/.local/share/solar-neo:\$PYTHONPATH"
python3 -m solarneo "\$@"
EOF

cat > "$DEST_BIN/sln" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="\$HOME/.local/share/solar-neo:\$PYTHONPATH"
python3 -m solarneo "\$@"
EOF

chmod +x "$DEST_BIN/solar" "$DEST_BIN/sln"

echo "✅ Solar Neo installed!"
echo "  - Core: $DEST_SHARE"
echo "  - CLI:  $DEST_BIN/solar"

# PATH Warning
if [[ ":$PATH:" != *":$DEST_BIN:"* ]]; then
    echo ""
    echo "⚠️  $DEST_BIN is not in your PATH"
    echo "   Add it by running:"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
else
    echo "✔ $DEST_BIN is in your PATH"
fi

echo ""
echo "Try: solar version"
echo "Try: solar sys"
