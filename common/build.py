#!/usr/bin/python3

import os
import glob
import sys
import colorama
from pprint import pprint
from colorama import Fore, Style

from lib.tasks import ExecType, Task
from lib.manifests import load_manifest
from lib.kconfiglib import kconfiglib
from lib.vars import kconfig_export_vars

colorama.init()

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
kconfig_export_vars(kconf)

DS_HOST_ROOT_PATH = os.environ['DS_HOST_ROOT_PATH']
DS_DL = os.environ['DS_DL']
DS_WORK = os.environ['DS_WORK']
DS_DISTRO = os.environ['DS_DISTRO']
DS_RELEASE = os.environ['DS_RELEASE']
DS_TARGET_ARCH = os.environ['DS_TARGET_ARCH']
DS_QEMU_STATIC = os.environ['DS_QEMU_STATIC']

tasks = []

# Generate the docker environment we use to build the kernel and userspace packages
tasks.append(Task(['common/host/build_host_docker.sh',
                   f"distros/{DS_DISTRO}/{DS_RELEASE}/host-{DS_TARGET_ARCH}-docker/"],
                   "Generating Host Docker image",
                   exectype = ExecType.HOST))

# Wipe the work directory from the docker. This directory has files owned by
# root, and docker lets us clean those.
tasks.append(Task(['rm', '-rf', '/work/work'],
                  "Cleaning old Work directory",
                   exectype = ExecType.DOCKER))
tasks.append(Task(['mkdir', '-p', DS_WORK],
                  "Creating new Work directory",
                   exectype = ExecType.HOST))
tasks.append(Task(['mkdir', '-p', f'{DS_WORK}/deploy'],
                  "Creating new work/deploy directory",
                   exectype = ExecType.HOST))
tasks.append(Task(['common/host/gen_docker_env.py'],
                  "Generate docker environment",
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
    if not manifest ['component_config'] or kconf.eval_string(manifest['component_config']) != 0:
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
                            exectype = ExecType.HOST))

        for i, docker_action in enumerate(docker_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{docker_action}", DS_HOST_ROOT_PATH)
            description = manifest['docker_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            exectype = ExecType.DOCKER))

        for i, chroot_script_action in enumerate(chroot_script_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{chroot_script_action}", DS_HOST_ROOT_PATH)
            description = manifest['chroot_script_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            exectype = ExecType.CHROOT_SCRIPT))

        for i, chroot_cmd_action in enumerate(chroot_cmd_actions):
            description = manifest['chroot_cmd_descriptions'][i]
            tasks.append(Task([chroot_cmd_action],
                            description,
                            exectype = ExecType.CHROOT_CMD))

# After we load all the tasks for kernel, distro, and packages, the next steps
# are to combine all the above installs and enter the chroot through qemu.
# When we are executing in the rootfs we can finish the apt installations
tasks.append(Task(['common/docker/combine_installs.sh'],
             "Combining package installations",
             exectype = ExecType.DOCKER))

# This sets up the qemu static binary, and sets up a few required /dev/ nodes
# We cannot execute CHROOT tasks until this is finished
tasks.append(Task(['common/docker/chroot_prep.sh'],
                  "Preparing chroot environment",
                  exectype = ExecType.DOCKER))

apt_task = Task(['common/chroot/apt_finish_install.sh'],
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
tasks.append(Task(['common/docker/chroot_clean.sh'],
                  "Cleaning up chroot environment",
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
