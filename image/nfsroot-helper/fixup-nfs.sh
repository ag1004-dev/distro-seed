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
    if [ ! -f "/etc/resolv.conf" ]; then
        # Create /etc/resolv.conf with the extracted DNS and search domain
        echo "nameserver \$dns" > /etc/resolv.conf
        echo "search \$search" >> /etc/resolv.conf
    fi
fi
EOF

chmod a+x "$runscript"
systemctl enable "$servicename"
