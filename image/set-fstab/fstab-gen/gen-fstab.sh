#!/bin/bash -e

INSTALL="$DS_WORK/deploy/80-fstab/"
mkdir -p "${INSTALL}/etc/"

cat > "${INSTALL}/etc/fstab" << EOF
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
$CONFIG_DS_FSTAB_GEN_ROOT_DEVICE /               $CONFIG_DS_FSTAB_GEN_ROOT_FS    $CONFIG_DS_FSTAB_GEN_ROOT_OPTIONS  0       1
EOF
