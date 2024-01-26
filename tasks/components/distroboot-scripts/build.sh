#!/bin/bash

install -d "$DS_OVERLAY/boot/"
mkimage -A arm -T script -C none -n 'boot' \
        -d "${DS_TASK_PATH}/files/boot.source" "${DS_OVERLAY}/boot/boot.scr"

if [[ "${CONFIG_DS_COMPONENT_DISTROBOOT_SCRIPTS_INSTALL_SOURCE}" == 'y' ]]; then
    install --target-directory="$DS_OVERLAY/boot/" "${DS_TASK_PATH}/files/boot.source"
fi
