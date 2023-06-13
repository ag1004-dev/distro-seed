#!/bin/bash -e

mkdir -p "${DS_OVERLAY}/etc/"
install -m 644 "$DS_FSTAB_FILE_PATH" "${DS_OVERLAY}/etc/fstab"
