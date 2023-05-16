#!/bin/bash -ex

if [ "$CONFIG_DS_XORG_STARTX_SERVICE_NO_DECORATIONS" = "y" ]; then
    WINDOW_MANAGER_COMMAND="matchbox-window-manager -use_cursor no -use_titlebar no &"
else
    WINDOW_MANAGER_COMMAND="matchbox-window-manager &"
fi

## Create x-session-manager script.  This is a shell script that would be changed to launch a user application
cat << EOF > /usr/bin/simple-x-session
#!/bin/sh

$WINDOW_MANAGER_COMMAND

# Set the root window's name to "xsm-ready"
xsetroot -name "xsm-ready"

# Wait for the window manager to be ready
while true; do
    if xwininfo -root -name "xsm-ready" >/dev/null 2>&1; then
        break
    fi
    sleep 0.1
done

# Set your application here. It must be run with 'exec'
# if this pid dies, the xserver will reset.

exec $CONFIG_DS_XORG_STARTX_SERVICE_TARGET
EOF

chmod a+x /usr/bin/simple-x-session
update-alternatives --install /usr/bin/x-session-manager x-session-manager /usr/bin/simple-x-session 50

# Create startup
cat << EOF > /etc/systemd/system/startx.service
[Unit]
Description=startx
After=systemd-user-sessions.service

[Service]
#User=
WorkingDirectory=~

Environment=XDG_SESSION_TYPE=x11
UnsetEnvironment=TERM

StandardOutput=journal
ExecStart=/usr/bin/startx -- vt8 -keeptty -verbose 3 -logfile /dev/null
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl enable startx.service
