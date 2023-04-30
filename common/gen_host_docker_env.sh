#!/bin/bash

# Write common environment variables to the env for docker
ENVFILE="$WORK/dockerenv"

# Paths should be updated to be relative to work
DL=${DL//$HOST_ROOT_PATH/\/work}
WORK=${WORK//$HOST_ROOT_PATH/\/work}
CACHE=${CACHE//$HOST_ROOT_PATH/\/work}

cat <<EOF > $ENVFILE
WORK=$WORK
DL=$DL
DISTRO=$DISTRO
CACHE=$CACHE
RELEASE=$RELEASE
TARGET_ARCH=$TARGET_ARCH
EOF
