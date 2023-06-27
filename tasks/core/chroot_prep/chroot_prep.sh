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
if [ -L "/etc/resolv.conf" ]; then
    install -d $(dirname $(readlink /etc/resolv.conf))
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
fi
