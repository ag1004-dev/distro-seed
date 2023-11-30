#!/bin/bash -e

SOURCE="$DS_WORK/kernel/linux/"
KERNEL_CACHE_KEY="$DS_WORK/kernel/linux-cache-key"

# Create caching key
install -d "$DS_WORK/kernel"

# If the url is a locally cloned git, we use the local head hash as the cache key
if [[ -d "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL" ]]; then
    pushd "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL" > /dev/null

    if [[ -n $(git status --porcelain --untracked-files=no) ]]; then
        echo "Error: Local Git repository is dirty. Please commit or stash your changes."
        exit 1
    fi

    if [[ -n "$CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION" ]]; then
        git checkout "$CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION"
    fi

    LOCAL_HEAD_HASH=$(git rev-parse HEAD)
    popd > /dev/null
    CACHE_KEY=$(common/host/gen_cache_key.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL $LOCAL_HEAD_HASH $CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION $CONFIG_DS_KERNEL_DEFCONFIG")
    echo "$CACHE_KEY" > "$KERNEL_CACHE_KEY"
    common/host/fetch_dir.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL" "$SOURCE"
else
        # Remote git
        CACHE_KEY=$(common/host/gen_cache_key.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL $CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION $CONFIG_DS_KERNEL_DEFCONFIG")
        echo "$CACHE_KEY" > "$KERNEL_CACHE_KEY"
        install -d "$SOURCE"
        common/host/fetch_git.sh "$CONFIG_DS_KERNEL_PROVIDER_GIT_URL" "$CONFIG_DS_KERNEL_PROVIDER_GIT_VERSION" "$SOURCE"
fi
