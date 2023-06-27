#!/bin/bash -e

if [ -e /etc/localtime ]; then
        rm /etc/localtime
fi
ln -s /usr/share/zoneinfo/${CONFIG_DS_TIMEZONE} /etc/localtime
