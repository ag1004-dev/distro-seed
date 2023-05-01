#!/bin/bash -e

if [[ "$JOURNAL_DISABLE_LOGS" == "y" ]]; then
    sed -i 's/#Storage=auto/Storage=none/' /etc/systemd/journald.conf
else
    journalctl "--vacuum-size=$JOURNAL_SIZE_VALUE"
fi
