#!/usr/bin/python3

import os
import sys
import subprocess
from kconfiglib import kconfiglib
import colorama

from lib.tasks import ExecType, Task

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')

if kconf.eval_string('ARCH_ARMHF') != '0':
    TARGET_ARCH='armhf'
elif kconf.eval_string('ARCH_ARMEL') != '0':
    TARGET_ARCH='armel'

if kconf.eval_string('DISTRO_DEBIAN_11') != '0':
    DISTRO='debian'
    RELEASE='bullseye'
elif kconf.eval_string('DISTRO_DEBIAN_12') != '0':
    DISTRO='debian'
    RELEASE='bookworm'
elif kconf.eval_string('DISTRO_UBUNTU_22_04') != '0':
    DISTRO='ubuntu'
    RELEASE='jammy'

host_root_path = os.path.dirname(os.path.abspath("__file__/"))
dl_dir = os.path.dirname(host_root_path + "/dl/")
work_path = os.path.dirname(host_root_path + "/work/")
cache_path = os.path.dirname(host_root_path + "/cache/")
host_docker_tag=f"distro-seed/{TARGET_ARCH}-{DISTRO}-{RELEASE}"

# Set common env variables, also write them to an env file
os.environ["WORK"] = work_path
os.environ["DL"] = dl_dir
os.environ["TAG"] = host_docker_tag
os.environ["CACHE"] = cache_path
os.environ["HOST_ROOT_PATH"] = host_root_path
os.environ["DISTRO"] = DISTRO
os.environ["RELEASE"] = RELEASE
os.environ["TARGET_ARCH"] = TARGET_ARCH

clear_task = Task(['rm', '-rf', '/work/work/'],
                 f'Clearing work',
                 exectype = ExecType.DOCKER)
clear_task.run()
