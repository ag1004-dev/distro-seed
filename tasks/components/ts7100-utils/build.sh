#!/bin/bash -e

SOURCE="$DS_WORK/components/ts7100-utils/"

cd "$SOURCE"

./autogen.sh
./configure --host="$AUTOTOOLS_HOST" --prefix="${DS_OVERLAY}/usr/local/"
make -j"$(nproc --all)" && make install
