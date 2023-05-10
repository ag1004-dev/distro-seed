#!/bin/bash -e

URL="https://files.embeddedts.com/ts-arm-sbc/ts-7970-linux/wifi-firmware/wl12xx-firmware-20170113.tar.xz"
INSTALL="$DS_WORK/deploy/50-wl12xx-firmware"
mkdir -p "$INSTALL/lib/firmware/"
common/host/fetch_tar.sh "$URL" "$INSTALL/lib/firmware/"
