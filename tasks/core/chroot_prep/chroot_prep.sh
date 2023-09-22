#!/bin/bash -e

# This command runs from the docker environment to prep the chroot environment
# to run further commands.

QEMU_STATIC_PATH=$(which ${DS_QEMU_STATIC})
cp "${QEMU_STATIC_PATH}" "${DS_WORK}/rootfs/${QEMU_STATIC_PATH}"

if [ ! -e "${DS_WORK}/rootfs/dev/zero" ]; then
    mknod -m 666 "${DS_WORK}/rootfs/dev/zero" c 1 5
fi
if [ ! -e "${DS_WORK}/rootfs/dev/null" ]; then
    mknod -m 666 "${DS_WORK}/rootfs/dev/null" c 1 3
fi

# Set up a temporary resolv.conf.
if [ -L "${DS_WORK}/rootfs/etc/resolv.conf" ]; then
    cd ${DS_WORK}/rootfs/etc/
    install -d $(dirname $(readlink resolv.conf))
    echo "nameserver 1.1.1.1" > "${DS_WORK}/rootfs/etc/resolv.conf"
fi

# The distro will ship its own sources.list
if [ -e "${DS_WORK}/rootfs/etc/apt/sources.list.d/multistrap-base.list" ]; then
    rm "${DS_WORK}/rootfs/etc/apt/sources.list.d/multistrap-base.list"
fi

# As an optimization for building images we do not want to honor fsync. This path
# is set from the dockerfile
if [ -e "${CROSS_EATMYDATALIB}" ]; then
    cp "${CROSS_EATMYDATALIB}" "${DS_WORK}/rootfs/eatmydata.so"
fi
