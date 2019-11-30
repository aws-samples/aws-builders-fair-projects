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

./stop.sh

if [ -f "/lib/systemd/system/greengrass.service" ]; then
  rm -f /lib/systemd/system/greengrass.service
  systemctl daemon-reload
fi

rm -rf /greengrass \
  ./bootstrap.json \
  ./config.json \
  ./core.private.key \
  ./core.cert.pem \
  ./greengrass-linux-aarch64-* \



