#!/bin/bash

export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
export LC_ALL=C LANGUAGE=C LANG=C
dpkg --configure -a
apt-get install -f
apt-get clean
passwd --delete root
chmod 755 /

# Set up a temporary resolv.conf.
if [ -L "/etc/resolv.conf" ]; then
    mkdir -p $(dirname $(readlink /etc/resolv.conf))
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
fi
