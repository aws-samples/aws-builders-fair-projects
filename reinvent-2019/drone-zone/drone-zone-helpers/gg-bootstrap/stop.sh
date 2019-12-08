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

if [ -f "/lib/systemd/system/greengrass.service" ]; then
    echo "Stopping with systemd"
    systemctl stop greengrass
else
    echo "Stopping manually"
    /greengrass/ggc/core/greengrassd stop
fi
