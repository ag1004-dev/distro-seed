#!/bin/bash

ROOTFS="$DS_WORK/rootfs/"
INSTALL="$DS_WORK/overlays/"

for dir in $INSTALL/*/
do
    cp -a "$dir"/. "$ROOTFS"
done
