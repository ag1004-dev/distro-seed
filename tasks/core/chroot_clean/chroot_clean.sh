#!/bin/bash

# This command runs from the docker environment to clean up anything left from
# the prep command

QEMU_STATIC_PATH=$(which ${DS_QEMU_STATIC})
rm "${DS_WORK}/rootfs/${QEMU_STATIC_PATH}"

# Clean up any directories that are normally tmpfs/devtmpfs
rm -rf ${DS_WORK}/rootfs/dev/*
rm -rf ${DS_WORK}/rootfs/tmp/*
rm -rf ${DS_WORK}/rootfs/run/*
