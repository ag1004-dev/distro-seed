#!/bin/bash -e

SOURCE="$DS_WORK/components/linux-firmware/"
GITURL="https://kernel.googlesource.com/pub/scm/linux/kernel/git/firmware/linux-firmware.git"
GITVERSION="20230804"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"

install -d "$DS_OVERLAY/lib/firmware/"

if [ "$CONFIG_DS_COMPONENT_LINUX_FIRMWARE_QCA9377" = "y" ]; then
        # Bluetooth
        install -d "$DS_OVERLAY/lib/firmware/qca"
        install -m 644 "${SOURCE}/qca/rampatch_00230302.bin" "$DS_OVERLAY/lib/firmware/qca/"
        install -m 644 "${SOURCE}/qca/nvm_00230302.bin" "$DS_OVERLAY/lib/firmware/qca/"
        # WIFI
        install -d "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0"
        install -m 644 "${SOURCE}/ath10k/QCA9377/hw1.0/board-2.bin" "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0/board-2.bin"
        install -m 644 "${SOURCE}/ath10k/QCA9377/hw1.0/board.bin" "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0/board.bin"
        install -m 644 "${SOURCE}/ath10k/QCA9377/hw1.0/firmware-5.bin" "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0/firmware-5.bin"
        install -m 644 "${SOURCE}/ath10k/QCA9377/hw1.0/firmware-6.bin" "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0/firmware-6.bin"
        install -m 644 "${SOURCE}/ath10k/QCA9377/hw1.0/firmware-sdio-5.bin" "$DS_OVERLAY/lib/firmware/ath10k/QCA9377/hw1.0/firmware-sdio-5.bin"
fi
