#!/bin/bash

if [ ! -e "/usr/sbin/sshd" ]; then
    echo -e "\n======================================================================="
    echo -e "\tsshd not installed in target!"
    echo -e "\tEither use a packagelist that includes sshd or disable"
    echo -e "\tDS_REGENERATE_SSH_KEYS in distro-seed config"
    echo -e "=======================================================================\n"
    exit 1
fi

servicename=sshkeys.service
servicefile="/etc/systemd/system/${servicename}"
runscript="/usr/local/bin/regen_ssh_keys"

rm -f /etc/ssh/ssh_host_*

cat <<EOF > "$servicefile"
[Unit]
Description=Regenerate SSH keys if they do not exist
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

EOF

chmod a+x "$runscript"
systemctl enable "$servicename"
