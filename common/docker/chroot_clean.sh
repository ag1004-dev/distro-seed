#!/bin/bash

# This command runs from the docker environment to clean up anything left from
# the prep command

QEMU_STATIC_PATH=$(which ${DS_QEMU_STATIC})
rm "${DS_WORK}/rootfs/${QEMU_STATIC_PATH}"
rm "${DS_WORK}/rootfs/dev/zero"
rm "${DS_WORK}/rootfs/dev/null"
