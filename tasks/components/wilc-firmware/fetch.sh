#!/bin/bash -e

URL="https://github.com/linux4wilc/firmware/archive/refs/tags/wilc_linux_16_1.tar.gz"
PRJ_WORK="$DS_WORK/wilc-firmware/"

install -d "$DS_OVERLAY/lib/firmware/mchp/"
install -d "$PRJ_WORK"

common/host/fetch_tar.sh "$URL" "$PRJ_WORK"

install -m 644 "${PRJ_WORK}/firmware-wilc_linux_16_1/wilc3000_ble_firmware.bin" "$DS_OVERLAY/lib/firmware/mchp/"
install -m 644 "${PRJ_WORK}/firmware-wilc_linux_16_1/wilc3000_wifi_firmware.bin" "$DS_OVERLAY/lib/firmware/mchp/"
install -m 644 "${PRJ_WORK}/firmware-wilc_linux_16_1/LICENSE.wilc_fw" "$DS_OVERLAY/lib/firmware/mchp/"
