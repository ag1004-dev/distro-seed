#!/bin/bash -e

ROOTFS="$WORK/rootfs/"
OUTPUT="$WORK/output/"
TARFILE="${OUTPUT}/rootfs.tar"

mkdir -p "$OUTPUT"

COMPRESSION=""

if [[ "$IMAGE_ROOTFS_TAR_NONE" ]]; then
        COMPRESSION=""
elif [[ "$IMAGE_ROOTFS_TAR_XZ" ]]; then
        COMPRESSION="J"
        TARFILE="${TARFILE}.xz"
elif [[ "$IMAGE_ROOTFS_TAR_BZIP2" ]]; then
        COMPRESSION="j"
        TARFILE="${TARFILE}.bz2"
else 
        echo "Invalid compresion!"
        exit 1
fi

cd $ROOTFS
tar c${COMPRESSION}f "$TARFILE" .
