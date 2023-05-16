#!/bin/bash -e

mkdir -p "$DS_OVERLAY/boot/"

wget -q \
     --output-document "${DS_OVERLAY}/boot/ts4900-fpga.bin" \
     https://files.embeddedts.com/ts-socket-macrocontrollers/ts-4900-linux/fpga/ts4900-fpga-20170510.bin
