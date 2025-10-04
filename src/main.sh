#!/usr/bin/env bash

# Usage: ./playblos.sh input.blos

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <input.blos>"
    exit 1
fi

input="$1"
base="$(basename "$input")"
tmpfile="$(mktemp --suffix=.wav)"
tmplog="$(mktemp --suffix=.log)"

# Decode .blos to temp wav
libblos -d "$input" "$tmpfile" > "$tmplog" 

# Run the Python player, pass wav as file and .blos name as display name
python3 ~/.local/bin/player-blos.py "$tmpfile" "${base%.blos}"

# Clean up temp wav after playback
rm -f "$tmpfile" "$tmplog"

