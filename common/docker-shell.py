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

HOST_ROOT_PATH = os.environ['HOST_ROOT_PATH']
WORK = os.environ['WORK']
TAG = os.environ['TAG']
dockerenv = os.path.abspath(WORK + "/dockerenv")

result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

os.execl(docker_path, 'docker', 'run', '-it',
         '--volume', f'{HOST_ROOT_PATH}:/work/',
         '--env-file', f'{dockerenv}',
         '--workdir', '/work/',
         TAG,
         'bash')