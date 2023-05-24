# Making a component:

Create a new folder in components/hello-world/
In that folder, make a Kconfig.  For example:
```
config COMPONENT_HELLO_WORLD
	bool "Component Test"
	help
	  A test component that populates /helloworld in the image

config COMPONENT_HELLO_WORLD_TEXT
	string "Hello world file text"
    help
      The text that goes in the hello world component
```

Edit /components/Kconfig and add with the other source commands:
```
source components/hello-world/Kconfig
```

Create a components/hello-world/manifest.py:
```
# This is the 'bool' config that causes this manifest.py to run
component_config = 'COMPONENT_HELLO_WORLD'
# This will execute this at a bash prompt, and print the description while it runs
chroot_cmd_actions = [ 'echo $CONFIG_DS_COMPONENT_HELLO_WORLD_TEXT > /helloworld' ]
chroot_cmd_descriptions = [ 'Populating /helloworld' ]

## We would include this if we wanted to copy a script into the chroot and execute
## it in the target rootfs.  This would get copied from components/hello-world/ to /
## in the target rootfs, and executed.  While it runs in the image generation
## we will print the description
#chroot_script_actions = [ 'script.sh' ]
#chroot_script_descriptions = [ 'Generating command-not-found database' ]

## We would include this if we have commands to run in the docker environment.  These
## Typically include any cross component compilation. This script must be under the
## path where distro-boot is checked out, it cannot access any location (eg /home/)
#docker_actions = [ 'script.sh' ]
#docker_descriptions = [ 'running script' ]

## We would add these if we wanted to run commands on the native host.  This 
## normally includes scripts that manage fetching a component's source to allow
## the host users git credentials to access any servers
#host_actions = [ 'script.sh' ]
#host_descriptions = [ 'running script' ]
