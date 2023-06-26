#!/bin/bash

SOURCE="$DS_WORK/components/ts7100-utils/"
GITURL="https://github.com/embeddedTS/ts7100-utils.git"
GITVERSION="v1.0.0"

install -d "$SOURCE"

common/host/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
