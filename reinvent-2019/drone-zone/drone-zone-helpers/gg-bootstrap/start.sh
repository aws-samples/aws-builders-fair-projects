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

sh -c "echo 1 > /proc/sys/fs/protected_hardlinks"
sh -c "echo 1 > /proc/sys/fs/protected_symlinks"

if [ -f "/lib/systemd/system/greengrass.service" ]; then
    echo "Starting with systemd"
    systemctl start greengrass
else
    echo "Starting manually"
    /greengrass/ggc/core/greengrassd start
fi

./monitor.sh

