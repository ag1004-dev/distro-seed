#!/bin/bash -e

SOURCE="$DS_WORK/components/wilc3000-external/"
# Kernel modules must install over existing kernel deploy to correctly provide
# module metadata (eg depmod, symvers, etc) for any external modules
INSTALL="$DS_WORK/deploy/10-kernel/"
KERNEL_SOURCE="$DS_WORK/kernel/linux/"
export KBUILD_OUTPUT="$DS_WORK/kernel/linux-kbuild/"
export CONFIG_WILC_SPI=m

cd "$KERNEL_SOURCE"
make M="$SOURCE" modules -j"$(nproc)"
make M="$SOURCE" INSTALL_MOD_PATH="$INSTALL" modules_install