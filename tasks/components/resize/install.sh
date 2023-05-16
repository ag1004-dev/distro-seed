#!/bin/bash -e

SCRIPT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
mkdir -p "$DS_OVERLAY/usr/local/bin/"
cp "$SCRIPT_PATH"/files/resize "$DS_OVERLAY/usr/local/bin/resize"
