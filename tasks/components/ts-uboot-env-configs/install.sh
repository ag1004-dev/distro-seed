#!/bin/bash -e

install -d "$DS_OVERLAY/usr/share/uboot-env-configs/"
install -m 644 "$DS_TASK_PATH"/files/* "$DS_OVERLAY/usr/share/uboot-env-configs/"
