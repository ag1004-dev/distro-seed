#!/bin/bash -e

MULTISTRAPCONF="$DS_WORK/multistrap.conf"
packagelist_file=packagelist/$CONFIG_DS_PACKAGELIST

if [ ! -e "$packagelist_file" ] && [ -n "$packagelist_file" ]; then
    echo "Specified packagelist \"$packagelist_file\" doesn't exist!"
    exit 1
fi

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
omitdebsrc=true
EOF
echo -n "packages=" >> "$MULTISTRAPCONF"

## Create combined packagelist from:
# base packagelist file
# $DS_WORK/packagelists/<files>
packagelist_combine=$(mktemp)
packagelist_tmp=$(mktemp)
cat "$packagelist_file" >> "$packagelist_tmp"

if [ -d "$DS_WORK/packagelist/" ]; then
    for file in $DS_WORK/packagelist/*; do
        cat "$file" >> "$packagelist_tmp"
        echo "" >> "$packagelist_tmp"
    done
fi

sed --in-place -e 's/#.*$//' -e '/^$/d' "${packagelist_tmp}" 

tr -s '[:space:]' ' ' < "$packagelist_tmp" > "$packagelist_combine"
packages=$(tr ' ' '\n' < "$packagelist_combine" | sort | uniq | paste -sd ' ' -)
echo "$packages" >> "$MULTISTRAPCONF"
rm "$packagelist_tmp" "$packagelist_combine"

cat <<EOF >> "$MULTISTRAPCONF"

source=${sourceurl}
keyring=${keyringname}
suite=${DS_RELEASE}
components=${deb_components}
EOF
