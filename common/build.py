#!/usr/bin/python3

import os
import glob
import sys
import subprocess
import colorama
from pprint import pprint
from colorama import Fore, Style

from lib.tasks import ExecType, Task
from lib.manifests import load_manifest
from lib.kconfiglib import kconfiglib
from lib.set_kconfig_vars import set_kconfig_vars

colorama.init()

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
set_kconfig_vars(kconf)

DS_HOST_ROOT_PATH = os.environ['DS_HOST_ROOT_PATH']
DS_DL = os.environ['DS_DL']
DS_WORK = os.environ['DS_WORK']
DS_DISTRO = os.environ['DS_DISTRO']
DS_RELEASE = os.environ['DS_RELEASE']
DS_TARGET_ARCH = os.environ['DS_TARGET_ARCH']
DS_QEMU_STATIC = os.environ['DS_QEMU_STATIC']

# Get all kconfig values in to key=value string list
config_dict={}
for key, value in kconf.syms.items():
    # Skip the preset MODULES symbol which does not apply here
    if key == 'MODULES':
        continue
    config_dict[f'CONFIG_{key}'] = value.str_value

tasks = []

# Generate the docker environment we use to build the kernel and userspace packages
tasks.append(Task(['common/build_host_docker.sh',
                   f"distros/{DS_DISTRO}/{DS_RELEASE}/host-{DS_TARGET_ARCH}-docker/"],
                   "Generating Host Docker image",
                   configs = config_dict,
                   exectype = ExecType.HOST))

# Wipe the work directory from the docker. This directory has files owned by
# root, and docker lets us clean those.
tasks.append(Task(['rm', '-rf', '/work/work'],
                  "Cleaning old Work directory",
                   exectype = ExecType.DOCKER))
tasks.append(Task(['mkdir', '-p', DS_WORK],
                  "Creating new Work directory",
                   exectype = ExecType.HOST))
# Generate docker environment file. This has to be done after the work
# directory is created
tasks.append(Task(['common/gen_host_docker_env.sh' ],
                   "Generating Docker environment file",
                   configs = config_dict,
                   exectype = ExecType.HOST))

# Add tasks in order of kernel/distros/packages
kernel_manifest_files = glob.glob(os.path.join('kernel', '**', 'manifest.py'),
                           recursive=True)
distro_manifest_files = glob.glob(os.path.join('distros', '**', 'manifest.py'),
                           recursive=True)
package_manifest_files = glob.glob(os.path.join('packages', '**', 'manifest.py'),
                           recursive=True)
image_manifest_files = glob.glob(os.path.join('image', '**', 'manifest.py'),
                           recursive=True)
generator_manifest_files = glob.glob(os.path.join('generators', '**', 'manifest.py'),
                           recursive=True)

# Process all the manifest files
manifests = [
    load_manifest(manifest_path)
    for manifest_path in kernel_manifest_files +
        distro_manifest_files +
        package_manifest_files +
        image_manifest_files + 
        generator_manifest_files
]

# Convert all of the manifest files into tasks
for manifest in manifests:
    if not manifest ['manifest_config'] or kconf.eval_string(manifest['manifest_config']) != 0:
        host_actions = manifest['host_actions']
        if manifest['host_actions'] is None:
            host_actions = []

        docker_actions = manifest['docker_actions']
        if manifest['docker_actions'] is None:
            docker_actions = []

        chroot_script_actions = manifest['chroot_script_actions']
        if manifest['chroot_script_actions'] is None:
            chroot_script_actions = []

        chroot_cmd_actions = manifest['chroot_cmd_actions']
        if manifest['chroot_cmd_actions'] is None:
            chroot_cmd_actions = []

        for i, host_action in enumerate(host_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{host_action}", DS_HOST_ROOT_PATH)
            description = manifest['host_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            configs=config_dict,
                            exectype = ExecType.HOST))

        for i, docker_action in enumerate(docker_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{docker_action}", DS_HOST_ROOT_PATH)
            description = manifest['docker_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            configs=config_dict,
                            exectype = ExecType.DOCKER))

        for i, chroot_script_action in enumerate(chroot_script_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{chroot_script_action}", DS_HOST_ROOT_PATH)
            description = manifest['chroot_script_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            configs=config_dict,
                            exectype = ExecType.CHROOT_SCRIPT))

        for i, chroot_cmd_action in enumerate(chroot_cmd_actions):
            description = manifest['chroot_cmd_descriptions'][i]
            tasks.append(Task([chroot_cmd_action],
                            description,
                            configs=config_dict,
                            exectype = ExecType.CHROOT_CMD))

# After we load all the tasks for kernel, distro, and packages, the next steps
# are to combine all the above installs and enter the chroot through qemu.
# When we are executing in the rootfs we can finish the apt installations
tasks.append(Task(['common/combine_installs.sh'],
             "Combining package installations",
             exectype = ExecType.DOCKER))

# Copy in QEMU static binary.  We cannot execute CHROOT types until this is done
which_result = subprocess.run(['which', DS_QEMU_STATIC], stdout=subprocess.PIPE, check = True)
qemu_static_path = which_result.stdout.decode().strip()
tasks.append(Task(['cp', qemu_static_path, f'/work/work/rootfs/{qemu_static_path}'],
                   "Setting up QEMU static binary in rootfs",
                   exectype = ExecType.DOCKER))

apt_task = Task(['common/apt_finish_install.sh'],
                   'Finishing apt install',
                   exectype = ExecType.CHROOT_SCRIPT)
tasks.append(apt_task)

# At this stage is when we want all CHROOT_CMD/Tasks to run., with the apt_task
# running first.
tasks = sorted(tasks, key=lambda task: (
    1 if task == apt_task else
    2 if task.exectype in (ExecType.CHROOT_SCRIPT, ExecType.CHROOT_CMD) else
    0
))

# Remove qemu static binary, no more CHROOT_ commands after this
tasks.append(Task(['rm', f'/work/work/rootfs/{qemu_static_path}'],
                   "Removing QEMU static binary in rootfs",
                   exectype = ExecType.DOCKER))

# Sort any task from generators/ to the end
tasks = sorted(tasks, key=lambda task: (
    1 if task.command[0].startswith('generator') else
    0
))

# Execute all tasks
for i, cmd in enumerate(tasks, start=1):
    config = {}

    if cmd.exectype == ExecType.HOST:
        TASKTYPE = "host"
    elif cmd.exectype == ExecType.DOCKER:
        TASKTYPE = "docker"
    elif cmd.exectype == ExecType.CHROOT_SCRIPT:
        TASKTYPE = "chroot_script"
    elif cmd.exectype == ExecType.CHROOT_CMD:
        TASKTYPE = "chroot_cmd"

    # Print out the description of the command
    print(f"Task ({TASKTYPE}) {i}/{len(tasks)}: {Fore.GREEN}{cmd.description}{Style.RESET_ALL}")

    #pprint(cmd.command)
    cmd.run()
