#!/bin/bash
#
# ensure-fw-env-config.sh - auto-create generate_fw_env_config
#
# This script currently supports only boards known to be built with
# U-Boot environments at 0x100000 and 0x180000. Many embeddedTS
# U-Boots, particularly many built before 2022, put their environments
# at 0x400000 and 0x600000, so beware of running
# `generate_fw_env_config -f` on older hardware!
#

if [ ! -e "/usr/bin/fw_printenv" ]; then
    echo "u-boot-tools is not installed"
    exit 1
fi

servicename=fwenvfirstboot.service
servicefile="/etc/systemd/system/${servicename}"
runscript="/usr/local/bin/generate_fw_env_config"

cat <<EOF > "$servicefile"
[Unit]
Description=Generate an appropriate fw_env.config at firstboot
ConditionPathExists=!/etc/fw_env.config

[Service]
Type=oneshot
ExecStart=${runscript}

[Install]
WantedBy=multi-user.target
EOF

cat <<FISH_HEADS > "$runscript"
#!/bin/bash
#
# generate_fw_env_config - creates /etc/fw_env.config
# By default, it only creates a file on boards that this script recognizes.
# Run it with '-f' to force it to create a (possibly wrong) file.
#

[ "\$1" = "-f" ] && RUNS_ON_THIS_BOARD=true || RUNS_ON_THIS_BOARD=false
eval \$(tshwctl -i)
# Add additional CMD lines below to recognize other board models.
# CMD >/dev/null && RUNS_ON_THIS_BOARD=true
echo "\${MODEL}" | grep '^71' >/dev/null && RUNS_ON_THIS_BOARD=true

! \${RUNS_ON_THIS_BOARD} && echo "Create /etc/fw_env.config manually when MODEL=\${MODEL}" && exit 0

EMMC_DEV=
[ -z "\${EMMC_DEV}" ] && [ "\${MODEL}" = "7180" ] && EMMC_DEV=1
[ -z "\${EMMC_DEV}" ] && [ "\${MODEL}" = "7120" ] && EMMC_DEV=1
[ -z "\${EMMC_DEV}" ] && EMMC_DEV=0

[ -f /etc/fw_env.config ] || cat > /etc/fw_env.config << EOF
# device             # offset     # size    # sector size
/dev/mmcblk\${EMMC_DEV}boot0    0x100000     0x20000   0x20000
/dev/mmcblk\${EMMC_DEV}boot0    0x180000     0x20000   0x20000
EOF

echo "Auto-created /etc/fw_env.config for MODEL=\${MODEL}"
FISH_HEADS

chmod a+x "$runscript"
systemctl enable "$servicename"
