"""
task.py - Module for defining and executing distro-seed tasks.

This module provides a Task class that represents a distro-seed task, which involves
the distribution and seeding of resources or data across a system or network. The
Task class provides a basic structure to define and execute such tasks.

Usage:
    # Import the Task class
    from task import Task
    from task_manager import Task

    prep_tasks = task_manager.load_tasks_from_manifest('tasks/core/chroot_prep/manifest.yaml')
    for prep in prep_tasks:
        prep.run()
"""

import os
import subprocess
from pprint import pprint

class Task:
    """Setup task to execute in different environments """

    def __init__(self, config, path, task_manifest):
        self.config = config
        self.dependencies = task_manifest.dependencies
        self.provides = task_manifest.provides
        self.path = path
        self.cmd_type = task_manifest.cmd_type
        self.cmd = task_manifest.cmd
        self.description = task_manifest.description
        self.enforce_dependencies = task_manifest.enforce_dependencies
        self.id = 0

    def run(self):
        """ Execute task in target environment """

        # These are placeholders only used for dependency tracking
        if self.cmd_type == 'dummy':
            return
    
        tag = os.environ.get('DS_TAG')
        ds_host_root_path = os.environ.get('DS_HOST_ROOT_PATH')
        work = os.environ.get('DS_WORK')
        dockerenv = os.path.abspath(work + "/dockerenv")
        full_cmd = os.path.relpath(
                f"{self.path}/{self.cmd}", ds_host_root_path)
        os.environ['DS_OVERLAY'] = os.path.abspath(work + f'/overlays/{self.id}-{self.config}')
        
        if not os.path.isfile(full_cmd):
            raise ValueError(f'{self.config} has task \"{full_cmd}\" that does not exist')

        if self.cmd_type == 'host':
            # If we're not using docker, add in any environment variables
            # and execute in our current env.  This is mostly just used
            # for fetches and early setup commands
            taskenv = os.environ.copy()
            subprocess.run(full_cmd, check=True, env=taskenv)
        elif self.cmd_type == 'target':
            # Copy the script to the chroot, execute it in the chroot, then
            # remove the script
            command = [ 'docker', 'run', '-it',
                        '--volume', f'{ds_host_root_path}:/work/',
                        '--workdir', '/work/', 
                        tag,
                        'cp', full_cmd, '/work/work/rootfs/run_in_chroot' ]
            subprocess.run(command, check=True)

            command = [
                'docker', 'run', '-it',
                '--volume', f'{ds_host_root_path}:/work/',
                '--workdir', '/work/',
                '--env-file', dockerenv,
                tag, 'chroot', '/work/work/rootfs',
                '/bin/bash', '-c', '/run_in_chroot'
            ]
            subprocess.run(command, check=True)

            command = [ 'docker', 'run', '-it',
                        '--volume', f'{ds_host_root_path}:/work/',
                        '--workdir', '/work/',
                        tag,
                        'rm', '/work/work/rootfs/run_in_chroot' ]
            subprocess.run(command, check=True)
        elif self.cmd_type == "docker":
            docker_task_cmd = f"{self.path}/{self.cmd}"

            command = [ 'docker', 'run', '-it',
                        '--volume', f'{ds_host_root_path}:/work/',
                        '--workdir', '/work/', ]

            # For the very first run we might not have a docker env file
            if os.path.exists(dockerenv):
                command += ['--env-file', dockerenv]

            ds_overlay_docker = os.environ['DS_OVERLAY'].replace(
                os.environ['DS_HOST_ROOT_PATH'], '/work')
            command += ['-e', f'DS_OVERLAY={ds_overlay_docker}']

            command += [tag] + [ '/work/' + docker_task_cmd ]
            subprocess.run(command, check=True)
        else:
            raise ValueError(f"Invalid cmd_type {self.cmd_type} from {self.config}")
