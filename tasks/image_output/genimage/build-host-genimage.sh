#!/bin/bash -e

SOURCE="$DS_WORK/components/host-genimage/"
CACHE_KEY=$(common/host/gen_cache_key.sh)

if ! common/host/fetch_cache_obj.sh "$CACHE_KEY" "$SOURCE"; then
    (
        cd "$SOURCE"
        ./autogen.sh
        ./configure
        make -j"$(nproc --all)"
    )
    common/host/store_cache_obj.sh "$CACHE_KEY" "$SOURCE"
fi
