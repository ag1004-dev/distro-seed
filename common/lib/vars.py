#!/usr/bin/python3

import os
import sys
from lib.kconfiglib import kconfiglib

def kconfig_export_vars(kconf):
    ''' Exports Kconfig options to the environment '''
    if kconf.eval_string('DS_ARCH_AARCH64') != 0:
        DS_TARGET_ARCH='arm64'
        DS_QEMU_STATIC='qemu-aarch64-static'
    elif kconf.eval_string('DS_ARCH_ARMHF') != 0:
        DS_TARGET_ARCH='armhf'
        DS_QEMU_STATIC='qemu-arm-static'
    elif kconf.eval_string('DS_ARCH_ARMEL') != 0:
        DS_TARGET_ARCH='armel'
        DS_QEMU_STATIC='qemu-armeb-static'
    else:
        print("Unsupported arch!")
        sys.exit(1)

    if kconf.eval_string('DS_DISTRO_DEBIAN_11') != 0:
        DS_DISTRO='debian'
        DS_RELEASE='bullseye'
    elif kconf.eval_string('DS_DISTRO_DEBIAN_12') != 0:
        DS_DISTRO='debian'
        DS_RELEASE='bookworm'
    elif kconf.eval_string('DS_DISTRO_UBUNTU_22_04') != 0:
        DS_DISTRO='ubuntu'
        DS_RELEASE='jammy'
    elif kconf.eval_string('DS_DISTRO_UBUNTU_23_04') != 0:
        DS_DISTRO='ubuntu'
        DS_RELEASE='lunar'
    else:
        print("Unsupported Distro!")
        sys.exit(1)

    DS_HOST_ROOT_PATH = os.path.dirname(os.path.abspath("__file__"))
    DS_DL = os.path.dirname(DS_HOST_ROOT_PATH + "/dl/")
    DS_WORK = os.path.dirname(DS_HOST_ROOT_PATH + "/work/")
    DS_CACHE = os.path.dirname(DS_HOST_ROOT_PATH + "/cache/")
    DS_TAG = f"distro-seed/{DS_TARGET_ARCH}-{DS_DISTRO}-{DS_RELEASE}"

    # Set common env variables
    os.environ["DS_WORK"] = DS_WORK
    os.environ["DS_DL"] = DS_DL
    os.environ["DS_TAG"] = DS_TAG
    os.environ["DS_CACHE"] = DS_CACHE
    os.environ["DS_HOST_ROOT_PATH"] = DS_HOST_ROOT_PATH
    os.environ["DS_DISTRO"] = DS_DISTRO
    os.environ["DS_RELEASE"] = DS_RELEASE
    os.environ["DS_TARGET_ARCH"] = DS_TARGET_ARCH
    os.environ["DS_QEMU_STATIC"] = DS_QEMU_STATIC
    # DS_OVERLAY is set in tasks.py at runtime

    # Set all config values
    for key, value in kconf.syms.items():
        # Skip the preset MODULES symbol which does not apply here
        if key == 'MODULES':
            continue
        os.environ[f'CONFIG_{key}'] = value.str_value
