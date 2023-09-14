#!/bin/sh -e

COMPONENT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
install -d "$DS_OVERLAY/etc/apt/"
install -m 644 "${COMPONENT_PATH}/files/sources.list" "$DS_OVERLAY/etc/apt/sources.list"
