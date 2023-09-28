#!/bin/bash -e

install -d "$DS_OVERLAY/etc/X11/Xsession.d/"
install -m 755 "$DS_TASK_PATH"/files/* "$DS_OVERLAY/etc/X11/Xsession.d/"
