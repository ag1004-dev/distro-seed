#!/bin/bash -e

INSTALL="$DS_WORK/deploy/80-fstab/"
mkdir -p "${INSTALL}/etc/"
cp "$DS_FSTAB_FILE_PATH" "${INSTALL}/etc/fstab"
