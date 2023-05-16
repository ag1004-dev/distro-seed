#!/bin/bash

SOURCE="$DS_WORK/kernel/linux/"
KBUILD_OUTPUT="$DS_WORK/kernel/linux-kbuild/"
KERNEL_CACHE_KEY="$(cat $DS_WORK/kernel/linux-cache-key)"
INSTALL="$DS_WORK/overlays/kernel/"

BUILD_OBJECT_KEY="linux-kernel-build-${KERNEL_CACHE_KEY}"
INSTALL_OBJECT_KEY="linux-kernel-install-${KERNEL_CACHE_KEY}"

# The kernel caching is a little unusual since we have two differnet objects to cache.
# The installed kernel+modules make up one cached object, and the build objects make up
# the other. We still need the build object in the cache to support building other modules
# that may use the kernel source as a dependency.
if ! common/host/fetch_cache_obj.sh "$BUILD_OBJECT_KEY" "$KBUILD_OUTPUT"; then
    export KBUILD_OUTPUT INSTALL
    (
        set +e
        cd "$SOURCE"
        # CROSS_COMPILE and ARCH are set from the dockerfile

        if [[ "$CONFIG_DS_KERNEL_INSTALL_ZIMAGE_FILESYSTEM" == 'y' ]]; then
            TARGETS="$TARGETS zImage"
        fi

        if [[ "$CONFIG_DS_KERNEL_INSTALL_UIMAGE_FILESYSTEM" == 'y' ]]; then
            export LOADADDR="$CONFIG_DS_KERNEL_INSTALL_UIMAGE_LOADADDR"
            TARGETS="$TARGETS uImage"
        fi

        make "$CONFIG_DS_KERNEL_DEFCONFIG"
        make -j"$(nproc --all)" all $TARGETS
    )
    common/host/store_cache_obj.sh "$BUILD_OBJECT_KEY" "$KBUILD_OUTPUT"
fi

if ! common/host/fetch_cache_obj.sh "$INSTALL_OBJECT_KEY" "$INSTALL"; then
    export KBUILD_OUTPUT INSTALL
    (
        set +e
        cd "$SOURCE"

        mkdir -p "${INSTALL}/boot"
        INSTALL_MOD_PATH="${INSTALL}" make modules_install

        if [[ "$DS_TARGET_ARCH" == "armel" || "$DS_TARGET_ARCH" == "armhf" ]]; then
            if [[ "$CONFIG_DS_KERNEL_INSTALL_ZIMAGE_FILESYSTEM" == 'y' ]]; then
                cp "$KBUILD_OUTPUT/arch/arm/boot/zImage" "${INSTALL}/boot/zImage"
            fi

            if [[ "$CONFIG_DS_KERNEL_INSTALL_UIMAGE_FILESYSTEM" == 'y' ]]; then
                cp "$KBUILD_OUTPUT/arch/arm/boot/uImage" "${INSTALL}/boot/uImage"
            fi
            
            for dtb in $CONFIG_DS_KERNEL_INSTALL_DEVICETREE_FILESYSTEM; do
                cp "$KBUILD_OUTPUT/arch/arm/boot/dts/${dtb}.dtb" "${INSTALL}/boot/"
            done
        else
            echo Unsupported arch
            exit 1
        fi
    )
    common/host/store_cache_obj.sh "$INSTALL_OBJECT_KEY" "$INSTALL"
fi
