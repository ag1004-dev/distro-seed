#!/bin/bash

sed -i -e "s/# $LOCALES.*/$LOCALES UTF-8/" /etc/locale.gen
dpkg-reconfigure --frontend=noninteractive locales
update-locale LANG=$LOCALES

if [[ "$PURGE_LOCALES" == "y" ]]; then
    locale-gen --purge $LOCALES
fi
