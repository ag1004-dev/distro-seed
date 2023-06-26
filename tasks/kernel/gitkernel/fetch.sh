#!/bin/bash -e

SOURCE="$DS_WORK/kernel/linux/"
KERNEL_CACHE_KEY="$DS_WORK/kernel/linux-cache-key"

# Create caching key
install -d "$DS_WORK/kernel"
CACHE_KEY=$(common/host/gen_cache_key.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL $CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION $CONFIG_DS_KERNEL_DEFCONFIG")
echo "$CACHE_KEY" > "$KERNEL_CACHE_KEY"

install -d "$SOURCE"
common/host/fetch_git.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL" "$CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION" "$SOURCE"
