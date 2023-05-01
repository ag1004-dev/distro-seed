#!/bin/bash

ROOTFS="$DS_WORK/rootfs/"
INSTALL="$DS_WORK/deploy/"

for dir in $INSTALL/*/
do
    cp -a "$dir"/. "$ROOTFS"
done
