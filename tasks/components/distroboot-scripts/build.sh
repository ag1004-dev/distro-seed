#!/bin/bash

COMPONENT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

install -d "$DS_OVERLAY/boot/"
mkimage -A arm -T script -C none -n 'boot' \
        -d "${COMPONENT_PATH}/files/boot.source" "${DS_OVERLAY}/boot/boot.scr"
