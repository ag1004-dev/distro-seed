#!/bin/bash -e

URL="https://github.com/linux4wilc/firmware/archive/refs/tags/wilc_linux_16_1.tar.gz"
PRJ_WORK="$DS_WORK/wilc-firmware/"

mkdir -p "$DS_OVERLAY/lib/firmware/mchp/"
mkdir -p "$PRJ_WORK"

common/host/fetch_tar.sh "$URL" "$PRJ_WORK"

cp "${PRJ_WORK}/firmware-wilc_linux_16_1/wilc3000_ble_firmware.bin" "$DS_OVERLAY/lib/firmware/mchp/"
cp "${PRJ_WORK}/firmware-wilc_linux_16_1/wilc3000_wifi_firmware.bin" "$DS_OVERLAY/lib/firmware/mchp/"
cp "${PRJ_WORK}/firmware-wilc_linux_16_1/LICENSE.wilc_fw" "$DS_OVERLAY/lib/firmware/mchp/"
