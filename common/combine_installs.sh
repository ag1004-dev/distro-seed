#!/bin/bash

ROOTFS="$WORK/rootfs/"
INSTALL="$WORK/deploy/"

for dir in $INSTALL/*/
do
    cp -a "$dir"/. "$ROOTFS"
done
