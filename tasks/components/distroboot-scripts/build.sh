#!/bin/bash

PACKAGE_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

mkdir -p "$DS_OVERLAY/boot/"
mkimage -A arm -T script -C none -n 'boot' \
        -d "${PACKAGE_PATH}/files/boot.source" "${DS_OVERLAY}/boot/boot.scr"
