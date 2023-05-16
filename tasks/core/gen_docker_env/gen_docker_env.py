#!/usr/bin/python3

import os
import path
import sys

libpath = os.path.dirname(os.environ['DS_HOST_ROOT_PATH'] + '/common/')
sys.path.append(libpath)

from lib.kconfiglib import kconfiglib

# Write common environment variables to the env for docker
envfile = os.path.join(os.environ['DS_WORK'], 'dockerenv')

# Paths should be updated to be relative to work
ds_dl = os.environ['DS_DL'].replace(os.environ['DS_HOST_ROOT_PATH'], '/work')
ds_work = os.environ['DS_WORK'].replace(os.environ['DS_HOST_ROOT_PATH'], '/work')
ds_cache = os.environ['DS_CACHE'].replace(os.environ['DS_HOST_ROOT_PATH'], '/work')

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')

with open(envfile, 'w') as f:
    f.write(f"DS_WORK={ds_work}\n")
    f.write(f"DS_DL={ds_dl}\n")
    f.write(f"DS_DISTRO={os.environ['DS_DISTRO']}\n")
    f.write(f"DS_CACHE={ds_cache}\n")
    f.write(f"DS_RELEASE={os.environ['DS_RELEASE']}\n")
    f.write(f"DS_TARGET_ARCH={os.environ['DS_TARGET_ARCH']}\n")
    f.write(f"DS_QEMU_STATIC={os.environ['DS_QEMU_STATIC']}\n")

    for key, value in kconf.syms.items():
        # Skip the preset MODULES symbol which does not apply here
        if key == 'MODULES':
            continue
        f.write(f'CONFIG_{key}={value.str_value}\n')
