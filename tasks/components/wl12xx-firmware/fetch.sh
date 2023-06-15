#!/bin/bash -e

URL="https://files.embeddedts.com/ts-arm-sbc/ts-7970-linux/wifi-firmware/wl12xx-firmware-20170113.tar.xz"
install -d "$DS_OVERLAY/lib/firmware/"
common/host/fetch_tar.sh "$URL" "$DS_OVERLAY/lib/firmware/"
