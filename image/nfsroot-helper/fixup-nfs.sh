#!/bin/bash -e

servicename=fixup-nfsboot.service
servicefile="/etc/systemd/system/${servicename}"
runscript="/usr/local/bin/fixup-nfsroot-dns.sh"

cat <<EOF > "$servicefile"
[Unit]
Description=Fixup networking on NFS boot

[Service]
Type=oneshot
ExecStart=/bin/bash ${runscript}
After=network-online.target
Wants=network-online.target

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > "$runscript"
# Check if nfsroot is present in /proc/cmdline
if grep -q "nfsroot" /proc/cmdline; then
    # Extract DNS and search domain from /proc/net/pnp
    dns=\$(awk '/^nameserver/ { print \$2 }' /proc/net/pnp)
    search=\$(awk '/^domain/ { print \$2 }' /proc/net/pnp)

    # Check if /etc/resolv.conf exists
    if [ ! -e "/etc/resolv.conf" ]; then
        # Create /etc/resolv.conf with the extracted DNS and search domain
        echo "nameserver \$dns" > /etc/resolv.conf
        echo "search \$search" >> /etc/resolv.conf
    else
        # resolved is likely controlling dns
        if ! resolvectl status | grep -q 'DNS Servers:'; then
            # Get a list of all network interfaces
            interfaces=(\$(ls /sys/class/net/))

            # Filter the list to only include interfaces that are up
            up_interfaces=()
            for interface in "\${interfaces[@]}"; do
            if [[ -f "/sys/class/net/\$interface/operstate" && \\
                    "\$(cat /sys/class/net/\$interface/operstate)" == "up" ]]; then
                up_interfaces+=("\$interface")
            fi
            done

            for interface in "\${up_interfaces[@]}"; do
                resolvectl dns \$interface \$dns
                if [ -n "\$search" ]; then
                    resolvectl domain \$interface \$search
                fi
            done
        fi
    fi
fi
EOF

chmod a+x "$runscript"
systemctl enable "$servicename"
