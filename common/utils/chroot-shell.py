#!/usr/bin/python3

import os
import sys
import subprocess

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from lib.kconfiglib import kconfiglib
from lib.task import Task
from lib import task_manager
from lib.vars import kconfig_export_vars

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
kconfig_export_vars(kconf)

host_root_path = os.environ['DS_HOST_ROOT_PATH']
work = os.environ['DS_WORK']
tag = os.environ['DS_TAG']
dockerenv = os.path.abspath(work + "/dockerenv")

# Get all kconfig values in to key=value string list
config_dict={}
for key, value in kconf.syms.items():
    # Skip the preset MODULES symbol which does not apply here
    if key == 'MODULES':
        continue
    config_dict[f'CONFIG_{key}'] = value.str_value

command = [
    'docker', 'run', '-it',
    '--volume', f'{host_root_path}:/work/',
    '--mount type=bind,src="/proc/",target=/work/work/rootfs/proc',
    '--workdir', '/work/',
    '--env-file', f'{dockerenv}',
    tag, 'chroot', '/work/work/rootfs', '/bin/bash'
]

result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

clean_tasks = task_manager.load_tasks_from_manifest('tasks/core/chroot_clean/manifest.yaml')
prep_tasks = task_manager.load_tasks_from_manifest('tasks/core/chroot_prep/manifest.yaml')
for prep in prep_tasks:
    prep.run()

ret = os.system(" ".join(command))

for clean in clean_tasks:
    clean.run()

sys.exit(ret)
