#!/usr/bin/env bash

# Check if we're root and re-execute if we're not.
rootcheck () {
    if [ $(id -u) != "0" ]
    then
        sudo "$0" "$@"  # Modified as suggested below.
        exit $?
    fi
}

rootcheck "${@}"

tail -F /greengrass/ggc/var/log/system/runtime.log
