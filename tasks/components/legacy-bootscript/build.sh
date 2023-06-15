#!/bin/bash -e

SOURCE="${DS_WORK}/legacy-bootscripts"

install -d "${DS_OVERLAY}/boot/"
install -d "$SOURCE"

echo "env set cmdline_append $CONFIG_DS_COMPONENT_LEGACY_BOOTSCRIPT_CMDLINE" > "${SOURCE}/boot.source"

mkimage -A arm -T script -C none -n 'boot' \
        -d "${SOURCE}/boot.source" "${DS_OVERLAY}/boot/boot.ub"

if [[ "$CONFIG_DS_COMPONENT_LEGACY_BOOTSCRIPT_INSTALL_SOURCE" == 'y' ]]; then
    install -m 644 "${SOURCE}/boot.source" "${DS_OVERLAY}/boot/"
fi
