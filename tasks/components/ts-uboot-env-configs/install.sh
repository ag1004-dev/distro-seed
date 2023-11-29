#!/bin/bash -e

install -d "$DS_OVERLAY/usr/share/uboot-env-configs/"

# install derefrences symlinks, so use cp to preserve symlinks here:
cp --no-dereference "$DS_TASK_PATH"/files/* "$DS_OVERLAY/usr/share/uboot-env-configs/"
chmod 644 $DS_OVERLAY/usr/share/uboot-env-configs/*

install -d "$DS_OVERLAY/usr/local/bin/"
install ${DS_TASK_PATH}/scripts/select_fw_env_config.sh "$DS_OVERLAY/usr/local/bin/select_fw_env_config"
