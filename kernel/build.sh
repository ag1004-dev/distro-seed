#!/bin/bash

SOURCE="$WORK/kernel/linux/"
KBUILD_OUTPUT="$WORK/kernel/linux-kbuild/"
KERNEL_CACHE_KEY="$(cat $WORK/kernel/linux-cache-key)"
INSTALL="$WORK/deploy/10-kernel/"

BUILD_OBJECT_KEY="linux-kernel-build-${KERNEL_CACHE_KEY}"
INSTALL_OBJECT_KEY="linux-kernel-install-${KERNEL_CACHE_KEY}"

# The kernel caching is a little unusual since we have two differnet objects to cache.
# The installed kernel+modules make up one cached object, and the build objects make up
# the other. We still need the build object in the cache to support building other modules
# that may use the kernel source as a dependency.
if ! common/fetch_cache_obj.sh "$BUILD_OBJECT_KEY" "$KBUILD_OUTPUT"; then
    export KBUILD_OUTPUT INSTALL
    (
        set +e
        cd "$SOURCE"
        # CROSS_COMPILE and ARCH are set from the dockerfile

        if [[ "$KERNEL_INSTALL_ZIMAGE_FILESYSTEM" == 'y' ]]; then
            TARGETS="$TARGETS zImage"
        fi

        if [[ "$KERNEL_INSTALL_UIMAGE_FILESYSTEM" == 'y' ]]; then
            export LOADADDR="$KERNEL_INSTALL_UIMAGE_LOADADDR"
            TARGETS="$TARGETS uImage"
        fi

        make "$KERNEL_DEFCONFIG"
        make -j"$(nproc --all)" all $TARGETS
    )
    common/store_cache_obj.sh "$BUILD_OBJECT_KEY" "$KBUILD_OUTPUT"
fi

if ! common/fetch_cache_obj.sh "$INSTALL_OBJECT_KEY" "$INSTALL"; then
    export KBUILD_OUTPUT INSTALL
    (
        set +e
        cd "$SOURCE"

        mkdir -p "${INSTALL}/boot"
        INSTALL_MOD_PATH="${INSTALL}" make modules_install

        if [[ "$TARGET_ARCH" == "armel" || "$TARGET_ARCH" == "armhf" ]]; then
            if [[ "$KERNEL_INSTALL_ZIMAGE_FILESYSTEM" == 'y' ]]; then
                cp "$KBUILD_OUTPUT/arch/arm/boot/zImage" "${INSTALL}/boot/zImage"
            fi

            if [[ "$KERNEL_INSTALL_UIMAGE_FILESYSTEM" == 'y' ]]; then
                cp "$KBUILD_OUTPUT/arch/arm/boot/uImage" "${INSTALL}/boot/uImage"
            fi
            
            for dtb in $KERNEL_INSTALL_DEVICETREE_FILESYSTEM; do
                cp "$KBUILD_OUTPUT/arch/arm/boot/dts/${dtb}.dtb" "${INSTALL}/boot/"
            done
        else
            echo Unsupported arch
            exit 1
        fi
    )
    common/store_cache_obj.sh "$INSTALL_OBJECT_KEY" "$INSTALL"
fi
