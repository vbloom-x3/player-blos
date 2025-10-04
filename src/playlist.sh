#!/bin/sh

playlist="$1"

if [ -z "$playlist" ]; then
    echo "Usage: $0 playlist.m3u8"
    exit 1
fi

while IFS= read -r file; do
    # skip comments or empty lines
    [ -z "$file" ] && continue
    case "$file" in
        \#*) continue ;;
    esac

    player-blos "$file"

done < "$playlist"
