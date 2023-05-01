import sys
import os
import shutil
import subprocess
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
    """Setup task to execute in different environments
    """
    def __init__(self, command, description, exectype=ExecType.HOST, relevant_configs = None):
        self.exectype = exectype
        self.relevant_configs = relevant_configs
        self.command = command
        if relevant_configs is None:
            self.relevant_configs = []
        else:
            self.relevant_configs = relevant_configs
        self.description = description
    
    def run(self, configs = None):
        """ Execute task in target environment
        """
        if configs is None:
            configs = []
        if self.exectype == ExecType.HOST:
            # If we're not using docker, add in any environment variables
            # and execute in our current env.  This is mostly just used
            # for fetches and early setup commands
            taskenv = os.environ.copy()
            taskenv.update(configs)
            subprocess.run(self.command, check=True, env=taskenv)
        elif self.exectype == ExecType.CHROOT_SCRIPT:
            # This executes in the target rootfs. This cmd must be a single
            # file we copy into the environment and execute. Eg,
            # a self contained bash or python script.
            tag = os.environ.get('TAG')
            prjroot = os.environ.get('HOST_ROOT_PATH')
            work = os.environ.get('WORK')
            rootfs = '/work/work/rootfs'
            chroot_cmd = os.path.abspath(work + "/rootfs/run_in_chroot")

            if (len(self.command) > 1):
                print("CHROOT_CMD must be a single script, see CHROOT_CMD")
                sys.exit(1)

            copy_task = Task(['cp', self.command[0],
                              '/work/work/rootfs/run_in_chroot'],
                              f'Chroot setup for: {self.description}',
                              exectype = ExecType.DOCKER)
            copy_task.run()

            chroot_cmd = ''
            for key, value in configs.items():
                chroot_cmd += (f"{key}=\"{value}\";")
            chroot_cmd += ('/run_in_chroot')

            command = [ 'docker', 'run', '-it',
                        '--volume', f'{prjroot}:/work/',
                        '--workdir', '/work/',
                        tag,
                        'chroot', rootfs, '/bin/bash', '-c', chroot_cmd ]

            subprocess.run(command, check=True)

            rm_task = Task(['rm', '/work/work/rootfs/run_in_chroot'],
                              f'Chroot setup for: {self.description}',
                              exectype = ExecType.DOCKER)
            rm_task.run()

        elif self.exectype == ExecType.CHROOT_CMD:
            # This executes in the target rootfs. This cmd must be a single
            # file we copy into the environment and execute. Eg,
            # a self contained bash or python script.
            tag = os.environ.get('TAG')
            prjroot = os.environ.get('HOST_ROOT_PATH')
            rootfs = '/work/work/rootfs'

            chroot_cmd = ''
            for key, value in configs.items():
                chroot_cmd += (f"{key}={value};")
            chroot_cmd += " ".join(self.command)

            command = [ 'docker', 'run', '-it',
                        '--volume', f'{prjroot}:/work/',
                        '--workdir', '/work/',
                        tag,
                        'chroot', rootfs, '/bin/bash', '-c', chroot_cmd ]

            subprocess.run(command, check=True)
        elif self.exectype == ExecType.DOCKER:
            tag = os.environ.get('TAG')
            prjroot = os.environ.get('HOST_ROOT_PATH')
            work = os.environ.get('WORK')
            dockerenv = os.path.abspath(work + "/dockerenv")
            command = [ 'docker', 'run', '-it',
                        '--volume', f'{prjroot}:/work/',
                        '--workdir', '/work/' ]

            # For the very first run we might not have a docker env file
            if os.path.exists(dockerenv):
                command.append('--env-file')
                command.append(f'{dockerenv}')

            if(configs):
                for key, value in configs.items():
                    command.append('-e')
                    command.append(f'{key}={value}')

            command.append(tag)
            command += self.command
            subprocess.run(command, check=True)
