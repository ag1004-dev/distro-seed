#!/bin/bash -e

SOURCE="${DS_WORK}/legacy-bootscripts"

mkdir -p "${DS_OVERLAY}/boot/"
mkdir -p "$SOURCE"

echo "env set cmdline_append $CONFIG_DS_PACKAGE_LEGACY_BOOTSCRIPT_CMDLINE" > "${SOURCE}/boot.source"

mkimage -A arm -T script -C none -n 'boot' \
        -d "${SOURCE}/boot.source" "${DS_OVERLAY}/boot/boot.ub"

if [[ "$CONFIG_DS_PACKAGE_LEGACY_BOOTSCRIPT_INSTALL_SOURCE" == 'y' ]]; then
    cp "${SOURCE}/boot.source" "${DS_OVERLAY}/boot/"
fi
