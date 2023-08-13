#!/usr/bin/env python3

import os
import sys
import subprocess
import colorama

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from lib.kconfiglib import kconfiglib
from lib.task import Task
from lib import task_manager
from lib.vars import kconfig_export_vars

kconf = kconfiglib.Kconfig('Kconfig')
kconf.load_config('.config')
kconfig_export_vars(kconf)

clean_tasks = task_manager.load_tasks_from_manifest('tasks/core/clear_cache/manifest.yaml')

for clean in clean_tasks:
    clean.run()
