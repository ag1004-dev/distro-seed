#!/bin/bash -e

SOURCE="$WORK/packages/ts4900-utils/"
INSTALL="$WORK/deploy/80-ts4900-utils/"

cd "$SOURCE"

./autogen.sh
./configure --bindir="${INSTALL}/usr/local/bin/"
make -j"$(nproc --all)" && make install
