#!/bin/bash -e

dockerpath="tasks/distros/${DS_DISTRO}/${DS_RELEASE}/host-${DS_TARGET_ARCH}-docker/"

if [[ ! -d "$dockerpath" ]]; then
    echo "Docker path ${dockerpath} does not exist!"
    exit 1;
fi

cd "$dockerpath"

if [[ "$(docker images -q $DS_TAG 2> /dev/null)" == "" ]]; then
    echo "Generating docker, this can take a while on the first build"
    docker build --tag "$DS_TAG" .
else
    # If the docker has already been built, this generally returns instantly.
    # In case there were changes though, we rebuild.
    docker build --quiet --tag "$DS_TAG" .
fi
