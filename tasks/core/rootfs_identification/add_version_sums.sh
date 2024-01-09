#!/bin/bash -e
#
# add_version_sums.sh - Final post-processing on rootfs before tar-ing it up
#

ROOTFS="${DS_WORK}/rootfs/"

cd "${ROOTFS}"
date +"%Y-%m-%d" > root.version
find . -type f \( ! -name md5sums.txt \) -print0 | xargs -0 md5sum > md5sums.txt
