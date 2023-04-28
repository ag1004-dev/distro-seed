#!/bin/bash

servicename=sshfirstboot.service
servicefile="/etc/systemd/system/${servicename}"
runscript="/usr/local/bin/regen_ssh_keys"

touch /ssh_regenkeys

cat <<EOF > "$servicefile"
[Unit]
Description=Regenerate SSH keys for first boot
ConditionPathExists=/ssh_regenkeys
Before=ssh.service

[Service]
Type=oneshot
ExecStart=${runscript}

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > "$runscript"
#!/bin/bash

if [ -e "/usr/sbin/sshd" ]; then
    ssh-keygen -A
fi

rm /ssh_regenkeys
EOF

chmod a+x "$runscript"
systemctl enable "$servicename"
