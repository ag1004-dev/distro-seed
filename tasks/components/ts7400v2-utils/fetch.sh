#!/bin/bash

SOURCE="$DS_WORK/components/ts7400v2-utils/"
GITURL="https://github.com/embeddedTS/ts7400v2-utils-linux4.x.git"
GITVERSION="v1.0.0"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
