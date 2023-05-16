#!/bin/bash -e

if [ ! -e /etc/locale.gen ]; then
    echo "locales package is not installed, skipping configuring locales"
    # this is not considered an error because locales configuration is not optional
    # if locales are installed.  Usually this should be included.
    exit 0
fi

sed -i -e "s/# $CONFIG_DS_LOCALES.*/$CONFIG_DS_LOCALES UTF-8/" /etc/locale.gen
dpkg-reconfigure --frontend=noninteractive locales
update-locale LANG=$CONFIG_DS_LOCALES

if [[ "$PURGE_LOCALES" == "y" ]]; then
    locale-gen --purge $CONFIG_DS_LOCALES
fi
