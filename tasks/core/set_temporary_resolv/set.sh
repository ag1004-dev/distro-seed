#!/bin/bash

# Set up a temporary resolv.conf.
if [ -L "/etc/resolv.conf" ]; then
    mkdir -p $(dirname $(readlink /etc/resolv.conf))
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
fi
