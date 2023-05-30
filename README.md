# distro-seed
## What is Distro-seed?
distro-seed is a tool to generate a Debian based distribution rootfs, similar to buildroot but using Debian packages. Right now this only targets cross platform targets like armhf.

This performs a series of tasks on a debian-based rootfs to generate the image.
* Tasks are configured through a Kconfig system using Kconfiglib
** For example:
*** Select Locales
*** Purge Man pages
*** Set journal log limits
* Docker is used to provide a compatible host environment to cross compile for your target environment
* Dependency tracking for more complex projects
* Packagelists are used to pick what packages are installed into a base image
* Caches build objects like kernel, or multistrap installs

# Installing:
This will run from any Linux distribution that supports Docker, python3, and has a filesystem with unix permissions.

* From Ubuntu/Debian based distros:
```
apt-get update && apt-get install -y qemu-user-static
```

* From Fedora/Redhat based distros:
```
dnf install qemu-user-static
```

Next install distro-seed, the python requirements and check the dependencies:
```
git clone https://github.com/embeddedTS/distro-seed.git
cd distro-seed
pip install -r requirements.txt
make checkdeps # Verifies all execution requirements are met
```

# Generating a rootfs:
To generate a rootfs for an embeddedTS i.MX6 platforms:

```
make tsimx6-debian-12-minimal_defconfig
make
ls work/output/rootfs.tar
```

Besides package downloads this will typically take around 5-30 minutes on a workstation to generate an image. This generates a simple rootfs that is capable of Networking, installs the kernel from git, and runs other setup.
