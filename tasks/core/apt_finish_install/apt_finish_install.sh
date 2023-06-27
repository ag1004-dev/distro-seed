#!/bin/bash

export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
export LC_ALL=C LANGUAGE=C LANG=C
dpkg --configure -a

if [ "$DS_DISTRO" == "ubuntu" ] && [ "$DS_RELEASE" == "lunar" ]; then
    # Workaround for:
    # Setting up sgml-base (1.31) ...
    # cannot open catalog directory /etc/sgml: No such file or directory at /usr/sbin/update-catalog line 299.
    mkdir /etc/sgml/
fi

apt-get install -f
apt-get clean
chmod 755 /

# Set up a temporary resolv.conf.
if [ -L "/etc/resolv.conf" ]; then
    install -d $(dirname $(readlink /etc/resolv.conf))
    echo "nameserver 1.1.1.1" > /etc/resolv.conf
fi
