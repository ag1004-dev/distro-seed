#!/bin/bash

echo "nameserver 1.1.1.1" > /etc/resolv.conf
apt-get update
update-command-not-found
rm /etc/resolv.conf
