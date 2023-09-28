#!/bin/sh -e

install -d "$DS_OVERLAY/etc/apt/"
install -m 644 "${DS_TASK_PATH}/files/sources.list" "$DS_OVERLAY/etc/apt/sources.list"
