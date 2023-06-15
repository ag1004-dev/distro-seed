#!/bin/bash -e

SCRIPT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
install -d "$DS_OVERLAY/usr/local/bin/"
install -m 755 "$SCRIPT_PATH"/files/resize "$DS_OVERLAY/usr/local/bin/resize"
