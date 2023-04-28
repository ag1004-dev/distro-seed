#!/bin/bash -e

SOURCE="$WORK/rootfs/"
packages=packagelist/$PACKAGELIST

echo "SOURCE: $SOURCE"
mkdir -p "$SOURCE"

if [[ "$DISTRO" == "debian" ]]; then
        keyringname="debian-archive-keyring"
        sourceurl="http://deb.debian.org/debian"
elif [[ "$DISTRO" == "ubuntu" ]]; then
        keyringname="ubuntu-keyring"
        sourceurl="http://www.ports.ubuntu.com/ubuntu-ports"
fi

MULTISTRAPCONF="$WORK/multistrap.conf"

cat <<EOF > "$MULTISTRAPCONF"
[General]
arch=${TARGET_ARCH}
directory=rootfs
cleanup=true
noauth=false
unpack=true
debootstrap=Base
aptsources=Base

[Base]
EOF
echo -n "packages=" >> "$MULTISTRAPCONF"
tr -s '[:space:]' ' ' < "${packages}" | tr -d '\n' >> "$MULTISTRAPCONF"

cat <<EOF >> "$MULTISTRAPCONF"

source=$sourceurl
keyring=$keyringname
suite=${RELEASE}
components=main contrib non-free
EOF

/usr/sbin/multistrap -f "$MULTISTRAPCONF" -d "$SOURCE"

