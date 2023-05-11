#!/bin/bash

rm /etc/localtime
ln -s /usr/share/zoneinfo/${CONFIG_DS_TIMEZONE} /etc/localtime
