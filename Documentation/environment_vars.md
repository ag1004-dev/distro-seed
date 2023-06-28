Every script run by distro-seed has access to these core set of environment variables:

| Variable | Host | Docker | Target | Description |
| - | - | - | - | - |
| DS_HOST_ROOT_PATH | X | X |   | Path to where distro-seed is checked out. |
| DS_DL             | X | X |   | This is where downloads should be stored. This should only be written from the host, not from a docker |
| DS_WORK           | X | X |   | Path to distro-seed/work directory |
| DS_DISTRO         | X | X | X | Distro name, eg "ubuntu" or "debian" |
| DS_RELEASE        | X | X | X | Release name, eg "bullseye", or "jammy" |
| DS_TARGET_ARCH    | X | X | X | Architecture name, eg "armhf" or "armel" |
| DS_OVERLAY        | X | X |   | Path to the overlay this project should use. Must create the directory manually |

The rest of the CONFIG options are also exported into each environment. For example a bool option in Kconfig will be y or n.  If a config file contains:
```
CONFIG_DS_JOURNAL_DISABLE_LOGS=y
```
This will be exported so it can be checked in any task with:
```
#!/bin/bash

if [ "$CONFIG_DS_JOURNAL_DISABLE_LOGS" = "y" ]; then
    echo "Option is enabled"
fi
```
Kconfig string values output the same way as bools, but with their value directly.
For example, the Kconfig option:
```
config DS_JOURNAL_SIZE_VALUE
	string "Set Journal size limit"
```
Is available in a script with:
```
echo "$CONFIG_DS_JOURNAL_SIZE_VALUE"
```

All config options are prefixed with "DS_" to avoid colliding with other Kconfig projects that might be built under distro-seed.
