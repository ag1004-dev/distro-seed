import sys
import os
import shutil
import subprocess
from pprint import pprint
from enum import Enum

class ExecType(Enum):
    """An enumeration of the possible execution types for a task.

    Attributes:
        HOST: Execute the command on the host. (Eg, most fetch tasks)
        DOCKER: The task should be executed inside a Docker container. 
        CHROOT_SCRIPT: Copy the script into the chroot, and execute it.
        CHROOT_CMD: Execute command at a bash prompt inside the target rootfs.
    """
    HOST = 0
    DOCKER = 1
    CHROOT_SCRIPT = 2
    CHROOT_CMD = 3

class Task:
    """Setup task to execute in different environments """
    def __init__(self, command, description, exectype=ExecType.HOST, configs = None):
        self.exectype = exectype
        self.command = command
        self.description = description
    
    def run(self):
        """ Execute task in target environment """

        tag = os.environ.get('DS_TAG')
        prjroot = os.environ.get('DS_HOST_ROOT_PATH')
        work = os.environ.get('DS_WORK')
        dockerenv = os.path.abspath(work + "/dockerenv")
        if self.exectype == ExecType.HOST:
            # If we're not using docker, add in any environment variables
            # and execute in our current env.  This is mostly just used
            # for fetches and early setup commands
            taskenv = os.environ.copy()
            subprocess.run(self.command, check=True, env=taskenv)
        elif self.exectype == ExecType.CHROOT_SCRIPT:
            # This executes in the target rootfs. This cmd must be a single
            # file we copy into the environment and execute. Eg,
            # a self contained bash or python script.

            if len(self.command) > 1:
                print("CHROOT_CMD must be a single script")
                sys.exit(1)

            copy_task = Task(['cp', self.command[0],
                              '/work/work/rootfs/run_in_chroot'],
                              f'Chroot setup for: {self.description}',
                              exectype = ExecType.DOCKER)
            copy_task.run()

            command = [
                'docker', 'run', '-it',
                '--volume', f'{prjroot}:/work/',
                '--workdir', '/work/',
                '--env-file', dockerenv,
                tag, 'chroot', '/work/work/rootfs',
                '/bin/bash', '-c', '/run_in_chroot'
            ]

            subprocess.run(command, check=True)
            rm_task = Task(['rm', '/work/work/rootfs/run_in_chroot'],
                           f'Chroot setup for: {self.description}',
                           exectype = ExecType.DOCKER)
            rm_task.run()
        elif self.exectype == ExecType.CHROOT_CMD:
            # This executes in the target rootfs. This cmd must be a single
            # file we copy into the environment and execute. Eg,
            # a self contained bash or python script.
            command = [
                'docker', 'run', '-it',
                '--volume', f'{prjroot}:/work/',
                '--workdir', '/work/',
                '--env-file', dockerenv,
                tag, 'chroot', '/work/work/rootfs',
                '/bin/bash', '-c'
            ]
            command += self.command

            subprocess.run(command, check=True)
        elif self.exectype == ExecType.DOCKER:
            command = [ 'docker', 'run', '-it',
                        '--volume', f'{prjroot}:/work/',
                        '--workdir', '/work/' ]

            # For the very first run we might not have a docker env file
            if os.path.exists(dockerenv):
                command += ['--env-file', dockerenv]

            command += [tag] + self.command
            subprocess.run(command, check=True)
