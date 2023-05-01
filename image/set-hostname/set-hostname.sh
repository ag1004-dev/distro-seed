#!/bin/bash

HOSTNAME="$CONFIG_DS_HOSTNAME"

if [[ -z "$HOSTNAME" ]]; then
    HOSTNAME="$DS_DISTRO-$DS_RELEASE-$DS_TARGET_ARCH"
fi

echo "$HOSTNAME" > /etc/hostname
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
