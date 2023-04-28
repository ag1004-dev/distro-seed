#!/bin/bash -ex

SOURCE="$WORK/kernel/linux/"

cd "$SOURCE"

# CROSS_COMPILE and ARCH are set from the dockerfile
make "$KERNEL_DEFCONFIG"
make -j"$(nproc --all)" all zImage

INSTALL="$WORK/deploy/10-kernel/"

mkdir -p "$INSTALL"/boot/
INSTALL_MOD_PATH="$INSTALL" make modules_install

if [[ "$TARGET_ARCH" == "armel" || "$TARGET_ARCH" == "armhf" ]]; then
    if [[ -n "$KERNEL_INSTALL_DEVICETREE_FILESYSTEM" ]]; then
        cp arch/arm/boot/zImage "$INSTALL"/boot/zImage
    fi
    
    for dtb in $KERNEL_INSTALL_DEVICETREE_FILESYSTEM; do
        cp "arch/arm/boot/dts/${dtb}.dtb" "$INSTALL"/boot/
    done
else
    echo Unsupported arch
    exit 1
fi
