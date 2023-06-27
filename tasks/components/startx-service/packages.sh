#!/bin/bash

# If the default "xterm" was left in place, lets make sure that is installed
if [ "$CONFIG_DS_XORG_STARTX_SERVICE_TARGET" = "xterm" ]; then
        echo "xterm"
fi

echo "matchbox-window-manager x11-xserver-utils"
