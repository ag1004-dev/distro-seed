#!/bin/sh -e

COMPONENT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
install -d "$DS_OVERLAY/etc/apt/sources.list.d/"
install -m 644 "${COMPONENT_PATH}/files/debian.sources" "$DS_OVERLAY/etc/apt/sources.list.d/debian.sources"
