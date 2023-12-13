#!/bin/bash -e

url="$1"
work_path="$2"
sha256sum="$3"

file_name=$(basename "$url")

file_dir="$DS_DL/blob"
file_path="$file_dir/$file_name"
install -d "$file_dir"

if [ ! -f "$file_path" ]; then
    wget -O "$file_path" "$url"
fi

if [ -z "$sha256sum" ]; then
    echo "Skipping checksum! No sha256sum provided for $file_name!"
    cp "$file_path" "$work_path"
    exit 0
fi

if echo "$sha256sum  $file_path" | sha256sum --quiet -c -; then
    cp "$file_path" "$work_path"
else
    echo "SHA256 of $file_name doesn't match provided SHA256 sum!"
    exit 1
fi
