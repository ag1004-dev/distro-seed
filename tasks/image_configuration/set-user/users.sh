#!/bin/bash -e

if [ "$CONFIG_DS_USER_ROOT_EN" = "y" ]; then
    # Permits passwordless login to root
    passwd --delete root
else
    usermod --shell /sbin/nologin root
fi

if [ -n "$CONFIG_DS_USER_ROOT_PASSWORD" ]; then
    echo root:password | chpasswd
fi

if [ "$CONFIG_DS_USER" = "y" ]; then
    # Warning, gecos is being replaced with --comment after Debian bookworm
    adduser --gecos "" --disabled-password "$CONFIG_DS_USER_NAME"
    echo "$CONFIG_DS_USER_NAME:$CONFIG_DS_USER_PASSWORD" | chpasswd

    if [ -z "$CONFIG_DS_USER_PASSWORD" ]; then
        passwd --delete "$CONFIG_DS_USER_NAME"
    fi

    if [ "$CONFIG_DS_USER_SUDO" = "y" ]; then
        usermod -aG sudo "$CONFIG_DS_USER_NAME"
    fi

    if [ -n "$CONFIG_DS_USER_GROUPS" ]; then
        # Trimming leading/trailing spaces
        CONFIG_DS_USER_GROUPS=$(echo "$CONFIG_DS_USER_GROUPS" | xargs)
        # Replacing spaces with commas
        CONFIG_DS_USER_GROUPS=$(echo "$CONFIG_DS_USER_GROUPS" | tr ' ' ',')
        usermod -G "$CONFIG_DS_USER_GROUPS" "$CONFIG_DS_USER_NAME"
    fi
fi
