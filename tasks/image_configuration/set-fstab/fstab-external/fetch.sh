#!/bin/bash -e

mkdir -p "${DS_OVERLAY}/etc/"
cp "$DS_FSTAB_FILE_PATH" "${DS_OVERLAY}/etc/fstab"
