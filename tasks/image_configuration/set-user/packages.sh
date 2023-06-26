#!/bin/bash

# Currently the sudo package is always sudo on any ubuntu/debian release
if [ "$CONFIG_DS_USER_SUDO" = "y" ]; then
        echo "sudo"
fi
