#!/bin/sh -e

install -d "$DS_OVERLAY/etc/apt/sources.list.d/"
install -m 644 "${DS_TASK_PATH}/files/debian.sources" "$DS_OVERLAY/etc/apt/sources.list.d/debian.sources"
