#!/bin/bash -e

INTERVAL=$((CONFIG_DS_WATCHDOG_TIMEOUT/4))
if ((INTERVAL < 1)); then
    INTERVAL=1
fi

# Write the configuration to /etc/watchdog.conf
cat > /etc/watchdog.conf << EOF
watchdog-device = $CONFIG_DS_WATCHDOG_DEVICE
watchdog-timeout = $CONFIG_DS_WATCHDOG_TIMEOUT
interval = $INTERVAL
realtime = yes
priority = 1
EOF
