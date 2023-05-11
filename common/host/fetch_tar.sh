#!/bin/bash -e

url="$1"
work_path="$2"

file_name=$(basename "$url")

file_path="$DS_DL/tar/$file_name"
mkdir -p "$DS_DL/tar/"

if [ -f "$file_path" ] && [ -f "${file_path}.sha256" ]; then
	set +e
	if sha256sum --quiet -c "$file_path.sha256"; then
		set -e
		tar -xf "$file_path" -C "$work_path"
		exit 0
	fi
fi

set -e

wget -O "$file_path" "$url"
sha256sum "$file_path" > "$file_path.sha256"
tar -xf "$file_path" -C "$work_path"
