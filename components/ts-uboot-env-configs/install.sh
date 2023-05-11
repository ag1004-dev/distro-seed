#!/bin/bash -e

INSTALL="$DS_WORK/deploy/ts-uboot-env-configs/"
PACKAGE_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
mkdir -p "$INSTALL/usr/share/uboot-env-configs/"
cp "$PACKAGE_PATH"/files/* "$INSTALL/usr/share/uboot-env-configs/"
