#!/bin/bash -e

INSTALL="$DS_WORK/deploy/50-ts4900-fpga"
mkdir -p "$INSTALL/boot/"

wget -q \
     --output-document "${INSTALL}/boot/ts4900-fpga.bin" \
     https://files.embeddedts.com/ts-socket-macrocontrollers/ts-4900-linux/fpga/ts4900-fpga-20170510.bin
