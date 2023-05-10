#!/bin/bash -e

SOURCE="$DS_WORK/components/ts4900-utils/"
INSTALL="$DS_WORK/deploy/80-ts4900-utils/"

cd "$SOURCE"

./autogen.sh
./configure --prefix="${INSTALL}/usr/local/"
make -j"$(nproc --all)" && make install
