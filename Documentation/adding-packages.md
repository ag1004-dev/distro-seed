# Making a package:

Create a new folder in packages/hello-world/
In that folder, make a Kconfig.  For example:
```
config PACKAGE_HELLO_WORLD
	bool "Package Test"
	help
	  A test package that populates /helloworld in the image

config PACKAGE_HELLO_WORLD_TEXT
	string "Hello world file text"
    help
      The text that goes in the hello world package
```

Edit /packages/Kconfig and add with the other source commands:
```
source packages/hello-world/Kconfig
```

Create a packages/hello-world/manifest.py:
```
# This is the 'bool' config that causes this manifest.py to run
manifest_config = 'PACKAGE_HELLO_WORLD'
# This will execute this at a bash prompt, and print the description while it runs
chroot_cmd_actions = [ 'echo $CONFIG_DS_PACKAGE_HELLO_WORLD_TEXT > /helloworld' ]
chroot_cmd_descriptions = [ 'Populating /helloworld' ]

## We would include this if we wanted to copy a script into the chroot and execute
## it in the target rootfs.  This would get copied from packages/hello-world/ to /
## in the target rootfs, and executed.  While it runs in the image generation
## we will print the description
#chroot_script_actions = [ 'script.sh' ]
#chroot_script_descriptions = [ 'Generating command-not-found database' ]

## We would include this if we have commands to run in the docker environment.  These
## Typically include any cross package compilation. This script must be under the
## path where distro-boot is checked out, it cannot access any location (eg /home/)
#docker_actions = [ 'script.sh' ]
#docker_descriptions = [ 'running script' ]

## We would add these if we wanted to run commands on the native host.  This 
## normally includes scripts that manage fetching a package's source to allow
## the host users git credentials to access any servers
#host_actions = [ 'script.sh' ]
#host_descriptions = [ 'running script' ]