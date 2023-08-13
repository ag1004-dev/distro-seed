# distro-seed
## What is Distro-seed?
distro-seed is a tool to generate a Debian based distribution image for embedded targets, similar to buildroot but using Debian packages. Right now this only targets cross platform targets like armhf/armel/arm64.

This performs a series of tasks on a debian-based rootfs to generate the image. The basic image is configured through a Kconfig system. Distro-seed provides hooks that can be used to apply overlays, execute commands in the target image, or otherwise update compile software for the target image.

Distro seed provides:
* Dependency resolution
* Debian packagelists (and further customization from the .config)
* Object and download caching

## Installing:
This will run from any Linux distribution that supports Docker, python3, and has a filesystem with unix permissions.

* From Ubuntu/Debian based distros:
```
apt-get update && apt-get install -y qemu-user-static
```

* From Fedora/Redhat based distros:
```
dnf install qemu-user-static
```

On either distribution, next install distro-seed, the python requirements and check the dependencies:
```
git clone https://github.com/embeddedTS/distro-seed.git
cd distro-seed
pip3 install --user -r requirements.txt
make checkdeps # Verifies all execution requirements are met
```
## Generating a rootfs:
```
make tsimx6_debian_12_x11_defconfig
make
# The resulting image will be in work/output/
```

Besides package downloads this will typically take around 5-30 minutes on a workstation to generate an image. This generates a simple rootfs that is capable of Networking, installs the kernel from git, and runs other setup.
