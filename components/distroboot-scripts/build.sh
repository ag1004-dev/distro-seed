#!/bin/bash

INSTALL="$DS_WORK/deploy/15-bootscripts/"
PACKAGE_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

mkdir -p "$INSTALL/boot/"

mkimage -A arm -T script -C none -n 'boot' \
        -d "${PACKAGE_PATH}/files/boot.source" "${INSTALL}/boot/boot.scr"
