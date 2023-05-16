#!/bin/bash

SOURCE="$DS_WORK/components/ts4900-utils/"
GITURL="https://github.com/embeddedTS/ts4900-utils.git"
GITVERSION="v1.0.0"

mkdir -p "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
