#!/bin/bash

KEY="$1"
TARGET="$2"

CACHE_FILE="${DS_CACHE}/${KEY}.tar.lz4"

mkdir -p "$DS_CACHE"
cd "$TARGET"
tar -c -I"lz4" --numeric-owner -f "$CACHE_FILE" .
