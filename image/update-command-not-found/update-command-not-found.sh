#!/bin/bash -e

if ! which update-command-not-found >/dev/null; then
        echo "command-not-found is not installed"
        exit 1
fi

echo "nameserver 1.1.1.1" > /etc/resolv.conf
apt-get update
update-command-not-found
rm /etc/resolv.conf
