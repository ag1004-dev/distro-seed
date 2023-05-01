#!/bin/bash

sed -i -e "s/# $SET_LOCALE_VALUE.*/$SET_LOCALE_VALUE UTF-8/" /etc/locale.gen
dpkg-reconfigure --frontend=noninteractive locales
update-locale LANG=$SET_LOCALE_VALUE

if [[ "$PURGE_LOCALES" == "y" ]]; then
    locale-gen --purge $SET_LOCALE_VALUE
fi
