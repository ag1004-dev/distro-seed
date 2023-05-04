# syntax = docker/dockerfile:1.2

FROM ubuntu:lunar

ENV chrootname armhf_ubuntu_lunar
RUN echo "PS1='${chrootname}\[\033[01;32m\]@\H\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /etc/bash.bashrc

RUN apt-get update && apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && echo 'LANG="en_US.UTF-8"'>/etc/default/locale && dpkg-reconfigure --frontend=noninteractive locales &&     update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
RUN apt-get update && apt-get install -y aptitude autogen automake bash bc bison build-essential bzip2 ca-certificates curl fakeroot file flex git gzip kmod libncursesw5-dev libssl-dev libtool lzop lz4 make multistrap ncurses-dev pkg-config qemu-user-static rsync runit u-boot-tools vim wget xz-utils

# Ubuntu has to fetch armhf from a different repo using ports.  We update the 
# existing sources.list to specify the architecture, then install the packages we need
RUN sed -i 's/deb http:\/\//deb [arch=amd64,i386] http:\/\//g' /etc/apt/sources.list
RUN printf "\ndeb [arch=armhf] http://ports.ubuntu.com/ jammy main universe multiverse" >> /etc/apt/sources.list
RUN dpkg --add-architecture armhf
RUN apt-get update
# This must be aptitude because it will have to downgrade some packges
# to install the armhf distribution
RUN aptitude install -y libgpiod-dev:armhf libc6:armhf libgcc-s1:armhf libstdc++6:armhf gcc-arm-linux-gnueabihf

# For linux cross compile
ENV CROSS_COMPILE=arm-linux-gnueabihf-
ENV ARCH=arm
# For autotools crosscompile
ENV host=arm-liux-gnueabihf
