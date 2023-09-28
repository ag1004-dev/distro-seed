#!/bin/bash

install -d "$DS_OVERLAY/etc/X11/xorg.conf.d/"
install -m 644 "${DS_TASK_PATH}"/files/*.conf "${DS_OVERLAY}/etc/X11/xorg.conf.d/"
