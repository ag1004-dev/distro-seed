#!/usr/bin/bash
#
# select_fw_env_config - choose a working fw_env.config to link to /run
# Copyright (c) 2024  Technologic Systems, Inc. dba embeddedTS
##
# The compatible string at the root of this board's device tree is used to
# determine what board model this is and hence where U-Boot may place its
# environment.
#
# The first matching candidate is used as a default if none are found to work,
# i.e. if the environment is uninitialized.
#
# If no candidates are found at all, a dummy file is written that gives a
# pointer on how to add the desired environment config file.
#
# If no /etc/fw_env.config exists at all, a symlink is created if possible,
# pointing to /run/fw_env.config.
#
# If a non-symlink /etc/fw_env.config file is present at /etc/fw_env.config, it
# is left alone.
#

if ! test -e /etc/fw_env.config && test -w /etc/ ; then
    echo "Create /etc/fw_env.config symlink"
    ln -s /run/fw_env.config /etc/fw_env.config
fi

if ! test -L /etc/fw_env.config ; then
    echo "Skip because /etc/fw_env.config file is not a symlink."
    exit 0
fi

env_config_dir=/usr/share/uboot-env-configs/

COMPATIBLE="$(cat /proc/device-tree/compatible | tr '\0' "\n" | head -1 | awk -F, '{print $2}')"

found=false
config_path=
default=
for try_path in $(find ${env_config_dir} | grep '/'${COMPATIBLE}'.*\.config$') ; do
    [ -z "${default}" ] && default="$(realpath ${try_path})"
    fw_printenv --config ${try_path} >/dev/null 2>&1 && found=true && config_path="$(realpath ${try_path})" && break
done

if ! ${found} ; then
    if [ -n "${default}" ] ; then
        config_path=${default}
        echo "No working fw_env.config found for this COMPATIBLE (=${COMPATIBLE}) in ${env_config_dir}; linking default (=$(basename ${config_path}))" >&2
    else
        echo "No matching fw_env.config found for this COMPATIBLE (=${COMPATIBLE}) in ${env_config_dir}; giving up." >&2
        cat >/run/fw_env.config <<EOF
# No matching fw_env.config found in ${env_config_dir} to match"
# this device's COMPATIBLE string (=${COMPATIBLE}).
#
# To fix: Place a correct u-boot environment config file named ${COMPATIBLE}.config
# into ${env_config_dir}"
EOF
        exit 1
    fi
fi
echo "Selected fw_env.config for COMPATIBLE=${COMPATIBLE}: $(basename ${config_path})"
ln -s ${config_path} /run/fw_env.config

exit 0
