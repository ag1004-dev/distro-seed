#!/bin/bash -e

INSTALL="$DS_WORK/deploy/50-resize"
PACKAGE_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

mkdir -p "$INSTALL/usr/local/bin/"

cp "$PACKAGE_PATH"/resize "$INSTALL/usr/local/bin/resize"
