# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

install_docker() {
  apt-get remove docker docker-engine docker.io
  apt-get update
  apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

  apt-key fingerprint 0EBFCD88

  sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

  apt-get update
  apt-get install -y docker-ce
}

set -e

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root"
  exit 1
fi

WORK_DIR=$(pwd)

if [ ! -f "$WORK_DIR/ev3dev.dockerfile" ]; then
  echo "Must be run in the same folder as a Dockerfile"
  exit 1
fi


if [ ! -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Installing..."
  install_docker
fi

# if [ ! -f "$WORK_DIR/qemu-arm-static" ]; then
#   echo "Building qemu..."
#   build_qemu $WORK_DIR
# fi

add-apt-repository ppa:ev3dev/tools -y
apt update -y
apt install brickstrap -y
chmod +r /boot/vmlinuz*


docker build --force-rm -t ev3-ros-melodic -f $WORK_DIR/ev3dev.dockerfile "$WORK_DIR"
