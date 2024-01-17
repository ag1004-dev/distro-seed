#!/bin/bash -e

SOURCE="$DS_WORK/components/ts7400v2-utils/"

cd "$SOURCE"

./autogen.sh
./configure --host="$AUTOTOOLS_HOST" --prefix="${DS_OVERLAY}/usr/local/"
make -j"$(nproc --all)" && make install
