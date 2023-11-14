#!/bin/bash

SOURCE="$DS_WORK/components/lv_drivers"
GITURL="https://github.com/lvgl/lv_drivers.git"
GITVERSION="v8.3.0"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
common/host/fetch_blob.sh "${CONFIG_DS_COMPONENT_LV_DRIVERS_LVDRVCONF}" "${SOURCE}/../"
