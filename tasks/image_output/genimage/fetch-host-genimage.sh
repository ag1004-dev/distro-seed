#!/bin/bash -e

SOURCE="$DS_WORK/components/host-genimage/"
GITURL="https://github.com/pengutronix/genimage.git"
GITVERSION="v16"

mkdir -p "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
