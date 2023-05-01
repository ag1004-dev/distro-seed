#!/bin/bash

rm /etc/localtime
ln -s /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
