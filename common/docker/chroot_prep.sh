#!/bin/bash -ex

# This command runs from the docker environment to prep the chroot environment
# to run further commands.

QEMU_STATIC_PATH=$(which ${DS_QEMU_STATIC})
cp "${QEMU_STATIC_PATH}" "${DS_WORK}/rootfs/${QEMU_STATIC_PATH}"

mknod -m 666 "${DS_WORK}/rootfs/dev/zero" c 1 5
mknod -m 666 "${DS_WORK}/rootfs/dev/null" c 1 3
