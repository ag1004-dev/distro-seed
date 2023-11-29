#!/bin/bash
#
# ensure-fw-env-config.sh - auto-create a service to run generate_fw_env_config at boot
#
# tasks/components/ts-uboot-env-configs
#

servicename=fw_env.service
servicefile="/etc/systemd/system/${servicename}"
runscript="/usr/local/bin/select_fw_env_config"

cat <<EOF > "$servicefile"
[Unit]
Description=Link to an appropriate fw_env.config
ConditionPathExists=!/run/fw_env.config

[Service]
Type=oneshot
ExecStart=${runscript}

[Install]
WantedBy=multi-user.target
EOF

ln -s /run/fw_env.config /etc/fw_env.config

systemctl enable "$servicename"
