#!/bin/bash -e

SOURCE="$DS_WORK/components/ts7553v2-utils/"
GITURL="https://github.com/embeddedTS/ts7553v2-utils.git"
GITVERSION="v1.0.0"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
