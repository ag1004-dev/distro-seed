#!/bin/bash

KEY="$1"
TARGET="$2"
CACHE_FILE="${DS_CACHE}/${KEY}.tar.lz4"

# Check integrity of lz4 archive
if lz4 -t "$CACHE_FILE" > /dev/null 2>&1; then
    install -d "$TARGET"
    if tar -x -I"lz4 -d" -f "$CACHE_FILE" -C "$TARGET"; then
        echo "Using Cached \"$TARGET\""
        exit 0
    fi
fi

exit 1
