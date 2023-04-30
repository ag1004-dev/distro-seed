import os
import sys
from lib.kconfiglib import kconfiglib

def set_kconfig_vars(kconf):
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

    HOST_ROOT_PATH = os.path.dirname(os.path.abspath("__file__"))
    DL = os.path.dirname(HOST_ROOT_PATH + "/dl/")
    WORK = os.path.dirname(HOST_ROOT_PATH + "/work/")
    CACHE = os.path.dirname(HOST_ROOT_PATH + "/cache/")
    TAG = f"distro-seed/{TARGET_ARCH}-{DISTRO}-{RELEASE}"

    # Set common env variables
    os.environ["WORK"] = WORK
    os.environ["DL"] = DL
    os.environ["TAG"] = TAG
    os.environ["CACHE"] = CACHE
    os.environ["HOST_ROOT_PATH"] = HOST_ROOT_PATH
    os.environ["DISTRO"] = DISTRO
    os.environ["RELEASE"] = RELEASE
    os.environ["TARGET_ARCH"] = TARGET_ARCH
    os.environ["QEMU_STATIC"] = QEMU_STATIC