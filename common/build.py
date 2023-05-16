#!/usr/bin/python3

import os
import glob
import sys
import argparse
import colorama
from pprint import pprint
from colorama import Fore, Style

from lib.kconfiglib import kconfiglib
from lib.task import Task
from lib import task_manager
from lib.vars import kconfig_export_vars

colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", action="store_true", help="Perform a dry run")
parser.add_argument("--plot-deps", action="store_true", help="Graph out dependencies")
args = parser.parse_args()

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

# Read in all manifests and create tasks for all of them
manifests = glob.glob(os.path.join('tasks', '**', 'manifest.yaml'), recursive=True)
for manifest_file in manifests:
    try:
        tasks += task_manager.load_tasks_from_manifest(manifest_file)
    except Exception as e:
        print(f"An error occurred while processing manifest '{manifest_file}': {str(e)}")
        sys.exit(1)

# Remove configs from the list that are not enabled in the config
tasks = [task for task in tasks if kconf.eval_string(task.config) != 0]

# Set default dependencies for each type of task.
for task in tasks:
    # Only set dependencies if there are none
    if len(task.dependencies) != 0:
        continue
    # Every other config will have dependencies except for 
    # DS_CORE_BUILD_HOST_DOCKER
    # Which will be sorted first
    if task.config == 'DS_CORE_BUILD_HOST_DOCKER':
        continue
    if task.cmd_type == 'host':
        task.dependencies += [ 'DS_WORK_READY' ]
    elif task.cmd_type == 'docker':
        task.dependencies += [ 'DS_DOCKER_READY' ]
    elif task.cmd_type == 'target':
        task.dependencies += [ 'DS_CHROOT_READY' ]
    else:
        raise ValueError(f"Invalid task type '{task.config.cmd_type}' in '{task.config}'")

if args.plot_deps:
    task_manager.print_deps(tasks)
    sys.exit(0)

# Sort tasks based on their dependencies
tasks = task_manager.sort(tasks)

# Execute all tasks
for i, task in enumerate(tasks, start=1):
    # Print out the description of the command
    print(f"Task: {task.config} ({task.cmd_type}) {i}/{len(tasks)}: {Fore.GREEN}{task.description}{Style.RESET_ALL}")
    if args.dry_run:
        pprint(f'{task.path}/{task.cmd}')
    else:
        try:
            task.run()
        except Exception as e:
            print(f"Task failed: {str(e)}")
            sys.exit(1)