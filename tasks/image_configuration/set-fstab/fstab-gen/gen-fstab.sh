#!/bin/bash -e

mkdir -p "${DS_OVERLAY}/etc/"
cat > "${DS_OVERLAY}/etc/fstab" << EOF
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
$CONFIG_DS_FSTAB_GEN_ROOT_DEVICE /               $CONFIG_DS_FSTAB_GEN_ROOT_FS    $CONFIG_DS_FSTAB_GEN_ROOT_OPTIONS  0       1
tmpfs                /var/volatile        tmpfs      defaults              0  0
tmpfs                /tmp                 tmpfs      defaults              0  0
EOF
