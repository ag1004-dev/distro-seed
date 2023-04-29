#!/usr/bin/python3

import sys
import os
import subprocess
import shutil
from colorama import Fore, Style

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
    print(f'{Fore.GREEN}Pass: The local filesystem is case sensitive.{Style.RESET_ALL}')
else:
    print(f'{Fore.RED}Fail: The local filesystem is not case sensitive.{Style.RESET_ALL}')
    print("This is not recommended to run from WSL, Cygwin, or network drive shares which")
    print("may not support typical unix permissions or case sensitivity. This can also")
    print("happen when using a fat32/ntfs or other case insensitive filesystem.")
    ret = 1

if run_hello_world_docker():
    print(f'{Fore.GREEN}Pass: Ran the hello-world docker.{Style.RESET_ALL}')
else:
    print(f'{Fore.RED}Fail: Failed to start docker.{Style.RESET_ALL}')
    print("Install docker using your distribution's docker package, or follow the")
    print("instructions here: https://docs.docker.com/engine/install/")
    ret = 1

if check_free_space():
    print(f"{Fore.GREEN}Pass: Sufficient free space{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Fail: Insufficient free space{Style.RESET_ALL}")
    print("Recommend having at minimum 40GB free")
    ret = 1

if check_bin_in_path('qemu-arm-static'):
    print(f"{Fore.GREEN}Pass: QEMU for armhf{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Fail: QEMU for armhf{Style.RESET_ALL}")
    print("qemu-arm-static is required on the host for armhf targets")
    printf("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if check_bin_in_path('qemu-armeb-static'):
    print(f"{Fore.GREEN}Pass: QEMU for armel{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Fail: QEMU for armel{Style.RESET_ALL}")
    print("qemu-armeb-static is required on the host for armel targets")
    printf("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if check_bin_in_path('qemu-aarch64-static'):
    print(f"{Fore.GREEN}Pass: QEMU for arm64{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Fail: QEMU for aarch64{Style.RESET_ALL}")
    print("qemu-armeb-static is required on the host for aarch64 targets")
    printf("Install your distribution's qemu static support, eg \'qemu-user-static\'")
    ret = 1

if not ret:
    print("All tests passed!")

sys.exit(ret)
