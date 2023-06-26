#!/bin/bash -e

TS7670_UBOOT_VERSION="20230301"
TS7670_UBOOT_SOURCE="ts7670-${TS7670_UBOOT_VERSION}.sd"
TS7670_UBOOT_SITE="https://files.embeddedts.com/ts-arm-sbc/ts-7670-linux/binaries/u-boot"
TS7670_UBOOT_SHA256="84f15ebb83b5711e827d2d20aba4cdab7b8f8907d82941ebc685a86892a12a0a"

URL="${TS7670_UBOOT_SITE}/${TS7670_UBOOT_SOURCE}"
PRJ_WORK="$DS_WORK/output/"

install -d "$PRJ_WORK"
common/host/fetch_blob.sh "$URL" "$PRJ_WORK/uboot.sd" "$TS7670_UBOOT_SHA256"
