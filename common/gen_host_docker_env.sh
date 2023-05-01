#!/bin/bash

# Write common environment variables to the env for docker
ENVFILE="$DS_WORK/dockerenv"

# Paths should be updated to be relative to work
DS_DL=${DS_DL//$DS_HOST_ROOT_PATH/\/work}
DS_WORK=${DS_WORK//$DS_HOST_ROOT_PATH/\/work}
DS_CACHE=${DS_CACHE//$DS_HOST_ROOT_PATH/\/work}

cat <<EOF > $ENVFILE
DS_WORK=$DS_WORK
DS_DL=$DS_DL
DS_DISTRO=$DS_DISTRO
DS_CACHE=$DS_CACHE
DS_RELEASE=$DS_RELEASE
DS_TARGET_ARCH=$DS_TARGET_ARCH
EOF
