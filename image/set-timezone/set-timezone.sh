#!/bin/bash

rm /etc/localtime
ln -s /usr/share/zoneinfo/${TIMEZONE_VALUE} /etc/localtime
