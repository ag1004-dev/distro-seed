#!/bin/bash -e

SOURCE="${DS_WORK}/kernel/linux/"
KERNEL_CACHE_KEY="${DS_WORK}/kernel/linux-cache-key"
GITURL="$CONFIG_DS_KERNEL_PROVIDER_GIT_URL"
GITVERSION="$CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION"

# Create caching key
mkdir -p "$DS_WORK/kernel"
# The key must include anything unique about this build
CACHE_KEY="$(common/gen_cache_key.sh $GITURL $GITVERSION $KERNEL_DEFCONFIG)"
echo "$CACHE_KEY" > "$KERNEL_CACHE_KEY"

mkdir -p "$SOURCE"

common/fetch_git.sh "$GITURL" "$GITVERSION" "$SOURCE"
