#!/usr/bin/python3

import os
import sys
import subprocess
from kconfiglib import kconfiglib
import colorama

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
host_docker_tag=f"distro-seed/{TARGET_ARCH}-{DISTRO}-{RELEASE}"
dockerenv = os.path.abspath(work_path + "/dockerenv")

result = subprocess.run(['which', 'docker'], capture_output=True,
                        text=True, check=True)
docker_path = result.stdout.strip()

os.execl(docker_path, 'docker', 'run', '-it',
         '--volume', f'{host_root_path}:/work/',
         '--env-file', f'{dockerenv}',
         '--workdir', '/work/',
         host_docker_tag,
         'chroot', '/work/work/rootfs', '/bin/bash' )