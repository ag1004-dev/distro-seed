#!/usr/bin/python3

import os
import sys
import subprocess
import colorama

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from lib.kconfiglib import kconfiglib
from lib.vars import kconfig_export_vars

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

command = [ 'docker', 'run', '--rm', '-it',
        '--volume', f'{HOST_ROOT_PATH}:/work/',
        '--workdir', '/work/' ]

# For the very first run we might not have a docker env file
if os.path.exists(dockerenv):
    command += ['--env-file', dockerenv]

command += [TAG, '/bin/bash']
result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

os.execl(docker_path, *command)
