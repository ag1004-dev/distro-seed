#!/bin/bash -e

INSTALL="$DS_WORK/rootfs/"
packagelist_file=packagelist/$CONFIG_DS_PACKAGELIST

mkdir -p "$INSTALL"

if [[ "$DS_DISTRO" == "debian" ]]; then
        keyringname="debian-archive-keyring"
        sourceurl="http://deb.debian.org/debian"
elif [[ "$DS_DISTRO" == "ubuntu" ]]; then
        keyringname="ubuntu-keyring"
        sourceurl="http://www.ports.ubuntu.com/ubuntu-ports"
fi

MULTISTRAPCONF="$DS_WORK/multistrap.conf"

cat <<EOF > "$MULTISTRAPCONF"
[General]
arch=${DS_TARGET_ARCH}
directory=rootfs
cleanup=true
noauth=false
unpack=true
debootstrap=Base
aptsources=Base

[Base]
EOF
echo -n "packages=" >> "$MULTISTRAPCONF"
tr -s '[:space:]' ' ' < "${packagelist_file}" | tr -d '\n' >> "$MULTISTRAPCONF"

cat <<EOF >> "$MULTISTRAPCONF"

source=${sourceurl}
keyring=${keyringname}
suite=${DS_RELEASE}
components=main contrib non-free
EOF

# For Debian based distributions we checksum the multistrap config
# which comprises our arch/distro/release/sourceurl/
DISTRO_CACHE_KEY=$(sha256sum $MULTISTRAPCONF | cut -f 1 -d ' ')
DISTRO_CACHE_KEY="${DS_DISTRO}-${DS_RELEASE}-${DS_TARGET_ARCH}-${DISTRO_CACHE_KEY}"

if ! common/fetch_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"; then
        /usr/sbin/multistrap -f "$MULTISTRAPCONF" -d "$INSTALL"
        common/store_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"
fi
