#!/bin/bash -e

INSTALL="$DS_WORK/rootfs/"
packagelist_file=packagelist/$CONFIG_DS_PACKAGELIST

mkdir -p "$INSTALL"

if [[ "$DS_DISTRO" == "debian" ]]; then
    keyringname="debian-archive-keyring"
    sourceurl="http://deb.debian.org/debian"
    if [[ "$DS_RELEASE" == "bullseye" ]]; then
        deb_components="main contrib non-free"
    else
        # After this release, debian split up non-free and non-free-firmware:
        # https://www.debian.org/releases/bookworm/armhf/release-notes/ch-information.html#non-free-split
        deb_components="main contrib non-free non-free-firmware"
    fi
elif [[ "$DS_DISTRO" == "ubuntu" ]]; then
    keyringname="ubuntu-keyring"
    sourceurl="http://www.ports.ubuntu.com/ubuntu-ports"
    deb_components="main universe multiverse"
else
    echo "Unknown distro \"$DS_DISTRO!"
    exit 1
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
# Skip anything between # and \n, and remove blank lines.
sed -e 's/#.*$//' "${packagelist_file}" | tr -s '[:space:]' ' ' | tr -d '\n' >> "$MULTISTRAPCONF"

cat <<EOF >> "$MULTISTRAPCONF"

source=${sourceurl}
keyring=${keyringname}
suite=${DS_RELEASE}
components=${deb_components}
EOF

# For Debian based distributions we checksum the multistrap config
# which comprises our arch/distro/release/sourceurl/
DISTRO_CACHE_KEY=$(sha256sum $MULTISTRAPCONF | cut -f 1 -d ' ')
DISTRO_CACHE_KEY="${DS_DISTRO}-${DS_RELEASE}-${DS_TARGET_ARCH}-${DISTRO_CACHE_KEY}"

if ! common/fetch_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"; then
    /usr/sbin/multistrap -f "$MULTISTRAPCONF" -d "$INSTALL"
    common/store_cache_obj.sh "$DISTRO_CACHE_KEY" "$INSTALL"
fi
