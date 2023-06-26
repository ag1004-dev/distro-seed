#!/bin/bash

# Set up a temporary resolv.conf.
if [ -L "/etc/resolv.conf" ]; then
    install -d $(dirname $(readlink /etc/resolv.conf))
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
fi
