#!/bin/bash -e
#
# add_version_sums.sh - Final post-processing on rootfs before tar-ing it up
#

ROOTFS="${DS_WORK}/rootfs/"

date +"%Y-%m-%d" > ${ROOTFS}/root.version
find . -type f -print0 | xargs -0 md5sum > ${ROOTFS}/md5sums.txt
