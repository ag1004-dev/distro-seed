#!/usr/bin/python3

import os
import sys
import subprocess
import colorama

from lib.kconfiglib import kconfiglib
from lib.set_kconfig_vars import set_kconfig_vars

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
set_kconfig_vars(kconf)

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

command = [ 'docker', 'run', '-it',
        '--volume', f'{HOST_ROOT_PATH}:/work/',
        '--workdir', '/work/' ]

if os.path.exists(dockerenv):
    command.append('--env-file')
    command.append(f'{dockerenv}')

for key, value in config_dict.items():
    command.append('-e')
    command.append(f'{key}={value}')

command.append(TAG)
command.append('/bin/bash')

result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

os.execl(docker_path, *command)
