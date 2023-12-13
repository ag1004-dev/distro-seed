#!/bin/bash

SOURCE="$DS_WORK/components/ts7100z-lvgl-ui-demo"
GITURL="https://github.com/embeddedts/ts7100z-lvgl-ui-demo"
GITVERSION="v1.0.0"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
