#!/usr/bin/python3

import os
import glob
import sys
from kconfiglib import kconfiglib
import subprocess
import colorama
from pprint import pprint
from colorama import Fore, Style

from lib.tasks import ExecType, Task
from lib.manifests import load_manifest

colorama.init()

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')

if kconf.eval_string('ARCH_ARMHF') != '0':
    TARGET_ARCH='armhf'
    QEMU_STATIC='qemu-arm-static'
elif kconf.eval_string('ARCH_ARMEL') != '0':
    TARGET_ARCH='armel'
    QEMU_STATIC='qemu-armeb-static'
else:
    print("Unsupported arch!")
    sys.exit(1)

if kconf.eval_string('DISTRO_DEBIAN_11') != '0':
    DISTRO='debian'
    RELEASE='bullseye'
elif kconf.eval_string('DISTRO_DEBIAN_12') != '0':
    DISTRO='debian'
    RELEASE='bookworm'
elif kconf.eval_string('DISTRO_UBUNTU_22_04') != '0':
    DISTRO='ubuntu'
    RELEASE='jammy'
else:
    print("Unsupported Distro!")
    sys.exit(1)

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

tasks = []

# Generate the docker environment we use to build the kernel and userspace packages
tasks.append(Task(['common/build_host_docker.sh',
                   f"distros/{DISTRO}/{RELEASE}/host-{TARGET_ARCH}-docker/"],
                   "Generating Host Docker image",
                   exectype = ExecType.HOST))

# Wipe the work directory from the docker. This directory has files owned by
# root, and docker lets us clean those.
tasks.append(Task(['rm', '-rf', '/work/work'],
                  "Cleaning old Work directory",
                   exectype = ExecType.DOCKER))
tasks.append(Task(['mkdir', '-p', work_path],
                  "Creating new Work directory",
                   exectype = ExecType.HOST))
# Generate docker environment file. This has to be done after the work
# directory is created
tasks.append(Task(['common/gen_host_docker_env.sh' ],
                   "Generating Docker environment file",
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
    if kconf.eval_string(manifest['manifest_config']) != 0:
        relevant_configs = []

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

        # Split config list in the manifest into a string array
        if manifest['relevant_configs']:
            relevant_configs = [x for x in manifest['relevant_configs'].split() if x]

        for i, host_action in enumerate(host_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{host_action}", host_root_path)
            description = manifest['host_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            relevant_configs=relevant_configs,
                            exectype = ExecType.HOST))

        for i, docker_action in enumerate(docker_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{docker_action}", host_root_path)
            description = manifest['docker_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            relevant_configs=relevant_configs,
                            exectype = ExecType.DOCKER))

        for i, chroot_script_action in enumerate(chroot_script_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{chroot_script_action}", host_root_path)
            description = manifest['chroot_script_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            relevant_configs=relevant_configs,
                            exectype = ExecType.CHROOT_SCRIPT))

        for i, chroot_cmd_action in enumerate(chroot_cmd_actions):
            cmdpath = os.path.relpath(
                f"{manifest['path']}/{chroot_cmd_action}", host_root_path)
            description = manifest['chroot_cmd_descriptions'][i]
            tasks.append(Task([cmdpath],
                            description,
                            relevant_configs=relevant_configs,
                            exectype = ExecType.CHROOT_CMD))

# After we load all the tasks for kernel, distro, and packages, the next steps
# are to combine all the above installs and enter the chroot through qemu.
# When we are executing in the rootfs we can finish the apt installations
tasks.append(Task(['common/combine_installs.sh'],
             "Combining package installations",
             exectype = ExecType.DOCKER))

# Copy in QEMU static binary.  We cannot execute CHROOT types until this is done
which_result = subprocess.run(['which', QEMU_STATIC], stdout=subprocess.PIPE, check = True)
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

    # Find any option configs for this package
    for relevant_config in cmd.relevant_configs:
        if relevant_config:
            config[relevant_config] = kconf.syms[relevant_config].str_value

    #pprint(cmd.command)
    cmd.run(config)
