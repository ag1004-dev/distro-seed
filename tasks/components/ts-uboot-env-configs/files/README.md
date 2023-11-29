A `fw_env.config` file is how **u-boot-tools** commands know the location
and other details of the U-Boot environment responsible for booting
this OS image.

While `u-boot-tools` expects this file to reside at
`/etc/fw_env.config`, that file cannot be altered when the root
filesystem is mounted read-only.  For that reason, the default
`/etc/fw_env.config` is a symlink to `/run/fw_env.config`, and that
file is determined at boot.

At boot, `/usr/local/bin/select_fw_env_config` uses the more specific part of the first "compatible" string to try and find the right config for your board. On any particular running system, this will show you that string:
```
cat /proc/device-tree/compatible | tr '\0' "\n" | head -1 | awk -F, '{print $2}'
```

When it is possible to encounter more than one layout, name the
configs with a number that causes them to sort in the order that they
should be tried (`${BOARD}-0.config`, `${BOARD}-1.config`, etc.).

If none of these environment configs are found to work (e.g., when no
environment has been saved yet), the first one tried will be chosen.

The `technologic-*.config` files contain the most common currently
shipping layouts and some recent past layouts. For convenience, you
can symlink one as your `${BOARD}.config`.
