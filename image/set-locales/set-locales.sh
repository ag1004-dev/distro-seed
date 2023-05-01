#!/bin/bash

sed -i -e "s/# $CONFIG_DS_LOCALES.*/$CONFIG_DS_LOCALES UTF-8/" /etc/locale.gen
dpkg-reconfigure --frontend=noninteractive locales
update-locale LANG=$CONFIG_DS_LOCALES

if [[ "$PURGE_LOCALES" == "y" ]]; then
    locale-gen --purge $CONFIG_DS_LOCALES
fi
