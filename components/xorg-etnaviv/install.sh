#!/bin/bash

INSTALL="$DS_WORK/deploy/xorg-etnaviv/"
PACKAGE_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

mkdir -p "$INSTALL/etc/X11/xorg.conf.d/"
cp "${PACKAGE_PATH}"/files/*.conf "${INSTALL}/etc/X11/xorg.conf.d/"
