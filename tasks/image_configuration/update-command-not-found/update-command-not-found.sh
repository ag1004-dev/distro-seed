#!/bin/bash -e

if ! which update-command-not-found >/dev/null; then
        echo "command-not-found is not installed"
        exit 1
fi

apt-get update
update-command-not-found
