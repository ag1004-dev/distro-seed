# Adding a custom component

Create a new folder in tasks/components/hello-world/. Any subfolder under tasks/ will work as well.

In that folder, make a Kconfig.  For example:
```
config DS_COMPONENT_HELLO_WORLD
	bool "Hello world"
	help
	  A test package that populates /helloworld in the image

config DS_COMPONENT_HELLO_WORLD_TEXT
	string "Hello world file text"
	depends on DS_COMPONENT_HELLO_WORLD
	default "Hello world!"
	help
	  The text that goes in the hello world package
```

Edit tasks/components/Kconfig and add with the other source commands:
```
source tasks/components/hello-world/Kconfig
```

Create a tasks/components/hello-world/manifest.yaml
```
config: DS_COMPONENT_HELLO_WORLD
tasks:
  - cmd: hello.sh
    cmd_type: target
    description: Running hello world process
```

The config line specifies which config causes this task to run. This must be enabled in the .config file through ```make menuconfig```. If this is not =y, none of the below steps are run.

The 'tasks:' section is a json list of tasks that will be run to complete this task. If the cmd_type and dependencies are the same for multiple tasks in a manifest they will be executed in order listed in this file.

The entry "cmd:" is the name of the script that should be run.  This path is relative to the manifest.yaml file.

The cmd_type specifies where that command should be run. This can be set to host, docker, target, dummy, or packagelist. These are described more in the yaml documentation, but this script will be run on "target" which is executed in the target image as if it were run on a board.

The description is printed out when a task is being run to show the user the current build step.

Next up, create the hello script tasks/components/hello-world/hello.sh:

```
#!/bin/bash

echo "$CONFIG_DS_COMPONENT_HELLO_WORLD_TEXT" > /helloworld
```

Make this script executable with:
```
chmod a+x tasks/components/hello-world/hello.sh
```

Finally, go into the menuconfig and enable this option we created. From the distro-seed root run:
```
# This can be replaced with any defconfig as an example
make tsimx6_debian_12_minimal_defconfig
# Enter the menuconfig to enable our option
make menuconfig
```
Enable the option under Components->Hello world, and optionally change the text under "Hello world file text".  Next, start a build:
```
make
```

After the build completes, the work/rootfs/ directory that shows the shipping filesystem will include a helloworld file.
