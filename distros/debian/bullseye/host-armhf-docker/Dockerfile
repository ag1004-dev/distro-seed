# syntax = docker/dockerfile:1.2

FROM debian:bullseye

ENV chrootname armhf_debian_bullseye
RUN echo "PS1='${chrootname}\[\033[01;32m\]@\H\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /etc/bash.bashrc

RUN apt-get update && apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && echo 'LANG="en_US.UTF-8"'>/etc/default/locale && dpkg-reconfigure --frontend=noninteractive locales &&     update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
RUN dpkg --add-architecture armhf
RUN apt-get update && apt-get install -y autogen automake bash bc bison build-essential bzip2 ca-certificates curl fakeroot file flex gcc-arm-linux-gnueabihf git gzip kmod libgpiod-dev:armhf libncursesw5-dev libssl-dev libtool lzop make multistrap ncurses-dev pkg-config python qemu-user-static rsync runit u-boot-tools vim wget xz-utils

# For linux cross compile
ENV CROSS_COMPILE=arm-linux-gnueabihf-
ENV ARCH=arm
# For autotools crosscompile
ENV host=arm-liux-gnueabihf
