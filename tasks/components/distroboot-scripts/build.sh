#!/bin/bash

install -d "$DS_OVERLAY/boot/"
mkimage -A arm -T script -C none -n 'boot' \
        -d "${DS_TASK_PATH}/files/boot.source" "${DS_OVERLAY}/boot/boot.scr"
