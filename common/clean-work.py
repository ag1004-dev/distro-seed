#!/usr/bin/python3

import os
import sys
import subprocess
import colorama

from lib.kconfiglib import kconfiglib
from lib.set_kconfig_vars import set_kconfig_vars
from lib.tasks import ExecType, Task

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
set_kconfig_vars(kconf)

clear_task = Task(['rm', '-rf', '/work/work/'],
                 f'Clearing work',
                 exectype = ExecType.DOCKER)
clear_task.run()
