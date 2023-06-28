The manifest.yaml specifies any tasks necessary to build an object. For example, this is an example software package yaml:

```
config: DS_COMPONENT_TSSUPERVISORUPDATE
tasks:
- cmd_type: host
  cmd: fetch.sh
  description: Downloading tssupervisorupdate
- cmd_type: docker
  cmd: build.sh
  description: Building tssupervisorupdate
```

# config
This option must match an option specified in Kconfig. Even if the option is not optional, it must have a Kconfig that enables it such as:
```
config DS_COMPONENT_TSSUPERVISORUPDATE
	bool
        default "y"
```
This would enable the config option without showing up in the menu, but satisy the kconfig symbol.

# tasks
The tasks are a json list of the fields described before.  A single manifest can include any number of tasks, but most are 1-3 at most.

## cmd_type
The cmdtype can be one of these 4 options:

* host
  * Executes the task on the host OS. Most fetch (like git clone, wget) should be run from the host to use any of the system's credentials or network configuration. The host task should not be used to build projects.
* docker
  * These are most commonly shell or python
  * Executes the "cmd" script in a docker matching the target distribution.  Most build tasks should run under docker.
  * For example, if the target is a Debian 12 armhf, the docker environment will match the host CPU but include the matching toolchain and libraries to cross compile for Debian 12. For example this would include libgpiod:armhf which can be used to cross compile applications using libgpiod with the matching library version that will be in the deployed image.
* target
  * These tasks are executed in the target rootfs. The task script specified in cmd is copied to work/rootfs/run_in_chroot, then [qemu's system emulation](https://www.qemu.org/docs/master/system/index.html) is used to chroot into this environment and execute this script.
  * Whenever possible target's "cmd" should point at a bash script for best compatibility between target distributions.
* dummy
  * These tasks perform nothing, and are only used for dependency synchronization.
* packagelist
  * The packagelist cmd executes on the host, but any stdout is used to select packages to end up in the target debian image.  For example, a packagelist cmd script that runs ```echo figlet``` would add the figlet package to the image.

## cmd
The cmd field is the name of the script to run. In general, this should point to a shell script, or python if it is a task run on the host.

## dependencies
This is a list of 'config' or 'provides' tasks that will be completed before this task. When not specified the 'dependencies' will be set to sane defaults based on the cmd_type to execute as soon as possible, and complete before moving onto the next stage of the image generation. Otherwise, dependencies looks for valid "config" tasks to execute before this task.

To show the dependencies, set up your .config and run:
```
make plotdeps
```
which will show a grahical representation of any dependencies.

## provides
This can be used to specify a name that can be used in dependencies. This is either used to allow multiple 'config' options to provide the same feature, or it can be used to create a dependency on an individual task rather than a config (which can contain multiple tasks)

## description
The description prints out during execution of a build to show the current task.

## auto_create_rdepends
This is used by core tasks to automatically create reverse dependencies to the children of its parent tasks that do not have children of their own. This makes sure all previous tasks are completed before proceeding.

To show the reverse dependencies, set up your .config and run:
```
make plotdeps
```
which will show a grahical representation of any dependencies. The tasks with green dotted lines are the tasks that are automatically added as reverse dependencies.
