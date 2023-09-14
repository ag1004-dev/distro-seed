#!/bin/bash -e

INSTALL="$DS_WORK/rootfs/"
MULTISTRAPCONF="$DS_WORK/multistrap.conf"
install -d "$INSTALL"

# For Debian based distributions we checksum the multistrap config
# which comprises our arch/distro/release/sourceurl/
DISTRO_CACHE_KEY=$(sha256sum $MULTISTRAPCONF | cut -f 1 -d ' ')
DISTRO_CACHE_KEY="distro-${DS_DISTRO}-${DS_RELEASE}-${DS_TARGET_ARCH}-${DISTRO_CACHE_KEY}"

if [ "$CONFIG_DS_DISTRO_NO_CACHE" = "y" ]; then
    /usr/sbin/multistrap -f "$MULTISTRAPCONF" -d "$INSTALL"
else
    if ! common/host/fetch_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"; then
        /usr/sbin/multistrap -f "$MULTISTRAPCONF" -d "$INSTALL"
        common/host/store_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"
    fi
fi
