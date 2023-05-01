#!/bin/bash -e

release="$1"
packagelist="$2"
sourceurl="$3"
keyringname="$4"
arch="$5"

cat <<EOF > "$DS_WORK/debian.conf"
[General]
arch=$arch
directory=rootfs
cleanup=true
noauth=false
unpack=true
debootstrap=Base
aptsources=Base

[Base]
EOF
echo -n "packages=" >> "$DS_WORK/debian.conf"
tr -s '[:space:]' ' ' < "$packagelist" | tr -d '\n' >> "$DS_WORK/debian.conf"

cat <<EOF >> "$DS_WORK/debian.conf"

source=$sourceurl
keyring=$keyringname
suite=$release
components=main contrib non-free
EOF
