#!/bin/bash -e

# Generate a sha256sum of all of the relevant unique factors that go into a cache object
KEYS="$@"
COMMON_KEYS="$DS_TARGET_ARCH $DS_RELEASE $DS_DISTRO $TAG" 
echo "$KEYS $COMMON_KEYS" | sha256sum | cut -f 1 -d ' '
