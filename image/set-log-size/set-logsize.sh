#!/bin/bash -e

if [[ "$CONFIG_DS_JOURNAL_DISABLE_LOGS" == "y" ]]; then
    sed -i 's/#Storage=auto/Storage=none/' /etc/systemd/journald.conf
else
    journalctl "--vacuum-size=$CONFIG_DS_JOURNAL_SIZE_VALUE"
fi
