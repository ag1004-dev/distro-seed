#!/usr/bin/python3

import sys
import os
import subprocess
import shutil
import importlib


def is_module_available(module_name):
    """
    Test if module can be imported
    """
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def is_filesystem_case_sensitive():
    """
    Checks if the local filesystem is case sensitive.
    """
    filename1 = 'testfile'
    filename2 = 'TESTFILE'
    
    # create files with the same name but different cases
    with open(filename1, 'w') as f1, open(filename2, 'w') as f2:
        f1.write('lower')
        f2.write('upper')
        
    # read the contents of the files and check if they match
    with open(filename1, 'r') as f1, open(filename2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
        contents_match = content1 == content2
        
    # remove the files
    os.remove(filename1)
    os.remove(filename2)
    
    return not contents_match

def run_hello_world_docker():
    """
    Runs the "hello world" Docker container and returns True if it succeeds.
    """
    try:
        # Run the "hello world" Docker container and capture both stdout and stderr
        result = subprocess.run(["docker", "run", "hello-world"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # If the command returns a non-zero exit code, the container failed to run
        print(e.stdout + e.stderr)
        return False
    else:
        # If the command returns a zero exit code, the container ran successfully
        return True

def check_free_space():
    """
    Checks whether the current directory has at least 40 GB of free space.
    Returns True if the free space is sufficient, and False otherwise.
    """
    path = os.getcwd()
    free_space = shutil.disk_usage(path).free / (1024 ** 3)  # Convert bytes to GB
    if free_space >= 40:
        return True
    else:
        return False

def check_bin_in_path(bin):
    """
    Checks whether the bin executable is in the `$PATH` environment variable.
    Returns True if it is found, and False otherwise.
    """
    paths = os.environ['PATH'].split(os.pathsep)
    for path in paths:
        bin_path = os.path.join(path, bin)
        if os.path.exists(bin_path) and os.access(bin_path, os.X_OK):
            return True
    return False

ret = 0

if is_filesystem_case_sensitive():
    print("Pass: The local filesystem is case sensitive.")
else:
    print("Fail: The local filesystem is not case sensitive.")
    print("This is not recommended to run from WSL, Cygwin, or network drive shares which")
    print("may not support typical unix permissions or case sensitivity. This can also")
    print("happen when using a fat32/ntfs or other case insensitive filesystem.")
    ret = 1

if run_hello_world_docker():
    print("Pass: Ran the hello-world docker.")
else:
    print("Fail: Failed to start docker.")
    print("Install docker using your distribution's docker package, or follow the")
    print("instructions here: https://docs.docker.com/engine/install/")
    ret = 1

if check_free_space():
    print("Pass: Sufficient free space")
else:
    print("Fail: Insufficient free space")
    print("Recommend having at minimum 40GB free")
    ret = 1

if check_bin_in_path('qemu-arm-static'):
    print("Pass: QEMU for armhf")
else:
    print("Fail: QEMU for armhf")
    print("qemu-arm-static is required on the host for armhf targets")
    print("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if check_bin_in_path('qemu-armeb-static'):
    print("Pass: QEMU for armel")
else:
    print("Fail: QEMU for armel")
    print("qemu-armeb-static is required on the host for armel targets")
    print("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if check_bin_in_path('sha256sum'):
    print("Pass: sha256sum available")
else:
    print("Fail: sha256sum missing")
    print("Install sha256sum for your host system")
    ret = 1

if is_module_available('colorama'):
    print("Pass: python 'colorama' module is available")
else:
    print("Fail: python 'colorama' module is not available")
    print("Try \"pip install -r requirements.txt\"")
    ret = 1

if is_module_available('path'):
    print("Pass: python 'path' module is available")
else:
    print("Fail: python 'path' module is not available")
    print("Try \"pip install -r requirements.txt\"")
    ret = 1

if is_module_available('yaml'):
    print("Pass: python 'yaml' module is available")
else:
    print("Fail: python 'yaml' module is not available")
    print("Try \"pip install -r requirements.txt\"")
    ret = 1

if is_module_available('matplotlib'):
    print("Pass: python 'matplotlib' module is available")
else:
    print("Fail: python 'matplotlib' module is not available")
    print("Try \"pip install -r requirements.txt\"")
    ret = 1

if is_module_available('networkx'):
    print("Pass: python 'networkx' module is available")
else:
    print("Fail: python 'networkx' module is not available")
    print("Try \"pip install -r requirements.txt\"")
    ret = 1

if check_bin_in_path('qemu-aarch64-static'):
    print("Pass: QEMU for arm64")
else:
    print("Fail: QEMU for aarch64")
    print("qemu-armeb-static is required on the host for aarch64 targets")
    print("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if not ret:
    print("All tests passed!")

sys.exit(ret)
