#!/bin/bash -e

git_url="$1"
git_version="$2"
work_path="$3"

prj_name=$(echo "$git_url" | sed 's/[^a-zA-Z0-9]/-/g')
git_path="$DS_DL/git/$prj_name"
mkdir -p "$DS_DL/git/"

if [[ -d "$git_path" ]]; then
    cd "$git_path"
    # If its already cloned, checkout the specified version.
    # If that fails, then we might have an old copy and we should
    # try to fetch that from the server. The hope is that we dont
    # have to prod a remote git server at all if we already have a checked 
    # out version
    set +e
    if ! git checkout "$git_version"; then
        set -e
        git fetch remote -a
        git reset --hard
        git checkout "$git_version"
    fi
else
    git clone "$git_url" "$git_path"
    cd "$git_path"
    git reset --hard
    git checkout "$git_version"
fi

mkdir -p "$work_path"
cp -a "$git_path/." "$work_path"
