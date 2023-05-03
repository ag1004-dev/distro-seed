#!/bin/bash

SOURCE="${DS_WORK}/legacy-bootscripts"
INSTALL="${DS_WORK}/deploy/15-legacy-bootscripts/"

mkdir -p "${INSTALL}/boot/"
mkdir -p "$SOURCE"

echo "env set cmdline_append $CONFIG_DS_PACKAGE_LEGACY_BOOTSCRIPT_CMDLINE" > "${SOURCE}/boot.source"

mkimage -A arm -T script -C none -n 'boot' \
        -d "${SOURCE}/boot.source" "${INSTALL}/boot/boot.ub"

if [[ "$CONFIG_DS_PACKAGE_LEGACY_BOOTSCRIPT_INSTALL_SOURCE" == 'y' ]]; then
    cp "${SOURCE}/boot.source" "${INSTALL}/"
fi
