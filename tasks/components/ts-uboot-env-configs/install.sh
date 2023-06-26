#!/bin/bash -e

COMPONENT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
isntall -d "$DS_OVERLAY/usr/share/uboot-env-configs/"
install -m 644 "$COMPONENT_PATH"/files/* "$DS_OVERLAY/usr/share/uboot-env-configs/"
