#!/bin/bash -e

SOURCE="$WORK/packages/ts4900-utils/"
INSTALL="$WORK/deploy/80-ts4900-utils/"

cd "$SOURCE"

./autogen.sh
./configure --prefix="${INSTALL}/usr/local/"
make -j"$(nproc --all)" && make install
