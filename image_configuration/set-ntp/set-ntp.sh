#!/bin/bash -e

cat <<EOF > /etc/systemd/system/timesyncd.conf
[Time]
NTP=$CONFIG_DS_USE_NTPSERVER_PROVIDER
EOF
