#!/bin/bash -e

COMPONENT_PATH=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
install -d "$DS_OVERLAY/etc/X11/Xsession.d/"
install -m 755 "$COMPONENT_PATH"/files/* "$DS_OVERLAY/etc/X11/Xsession.d/"
