#!/bin/bash

HOSTNAME="$SET_HOSTNAME_VALUE"

if [[ -z "$HOSTNAME" ]]; then
    HOSTNAME="$DISTRO-$RELEASE-$TARGET_ARCH"
fi

echo "$HOSTNAME" > /etc/hostname
echo "127.0.0.1 $HOSTNAME" >> /etc/hosts
