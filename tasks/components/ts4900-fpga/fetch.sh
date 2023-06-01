#!/bin/bash -e

URL="https://files.embeddedts.com/ts-socket-macrocontrollers/ts-4900-linux/fpga/ts4900-fpga-20170510.bin"
SHA256="f15edd6813ee5e93e7f380d85df2dc31e764ebca465093fb9006d56ee15b476b"

mkdir -p "$DS_OVERLAY/boot/"

common/host/fetch_blob.sh "$URL" "$DS_OVERLAY/boot/ts4900-fpga.bin" "$SHA256"
