#!/bin/bash

SOURCE="$DS_WORK/components/lvgl"
GITURL="https://github.com/lvgl/lvgl.git"
GITVERSION="v8.3.9"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
common/host/fetch_blob.sh "${CONFIG_DS_COMPONENT_LIBLVGL_LVCONF}" "${SOURCE}"
