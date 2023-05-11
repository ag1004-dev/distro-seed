#!/usr/bin/python3

import os
import sys
import subprocess

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from lib.kconfiglib import kconfiglib
from lib.vars import kconfig_export_vars
from lib.tasks import ExecType, Task

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
kconfig_export_vars(kconf)

HOST_ROOT_PATH = os.environ['DS_HOST_ROOT_PATH']
WORK = os.environ['DS_WORK']
TAG = os.environ['DS_TAG']
dockerenv = os.path.abspath(WORK + "/dockerenv")

# Get all kconfig values in to key=value string list
config_dict={}
for key, value in kconf.syms.items():
    # Skip the preset MODULES symbol which does not apply here
    if key == 'MODULES':
        continue
    config_dict[f'CONFIG_{key}'] = value.str_value

command = [
    'docker', 'run', '-it',
    '--volume', f'{HOST_ROOT_PATH}:/work/',
    '--workdir', '/work/',
    '--env-file', f'{dockerenv}',
    f'{TAG}', 'chroot', '/work/work/rootfs', '/bin/bash'
]

result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

prep = Task(['common/docker/chroot_prep.sh'],
            "Preparing chroot environment",
            exectype = ExecType.DOCKER)
clean = Task(['common/docker/chroot_clean.sh'],
               "Cleaning up chroot environment",
               exectype = ExecType.DOCKER)
prep.run()
ret = os.system(" ".join(command))
clean.run()

sys.exit(ret)
