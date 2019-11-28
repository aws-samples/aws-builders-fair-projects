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

# Install dependecies
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade

# list of packages to be installed
packagelist=(
  cmake
  google-mock
  libapr1-dev
  libaprutil1-dev
  libboost-all-dev
  libbz2-dev
  libconsole-bridge-dev
  libgpgme-dev
  libgtest-dev
  liblog4cxx-dev
  liblz4-dev
  libpoco-dev
  libssl-dev
  libtinyxml2-dev
  pkg-config
  python-catkin-pkg
  python-coverage
  python-defusedxml
  python-empy
  python-gnupg
  python-imaging
  python-mock
  python-netifaces
  python-nose
  python-numpy
  python-paramiko
  python-pip
  python-rosdep
  python-rospkg
  python-yaml
  python3-pip
  python3-yaml
)

apt-get install -y ${packagelist[@]}


# Upgrade pip version
pip install --upgrade setuptools

# Use pip to intall ros
pip install -U rosdep rosinstall_generator wstool rosinstall

# Use pip3 to install python 3 ros package
pip3 install -U rospkg catkin_pkg

# Install sbcl
wget http://netcologne.dl.sourceforge.net/project/sbcl/sbcl/1.2.7/sbcl-1.2.7-armel-linux-binary.tar.bz2
tar -xjf sbcl-1.2.7-armel-linux-binary.tar.bz2
cd sbcl-1.2.7-armel-linux
chmod +x install.sh
INSTALL_ROOT=/usr/local
./install.sh
cd ..

# Initiallize ros
rosdep init
echo -e "sbcl:\n  debian:\n    stretch: []" > /etc/ros/rosdep/ev3dev.yaml
echo "yaml file:///etc/ros/rosdep/ev3dev.yaml" >> /etc/ros/rosdep/sources.list.d/20-default.list


# Switch to robot user and build ros
sudo -i -u robot bash << EOF
rosdep update

mkdir ~/ros_catkin_ws
cd ~/ros_catkin_ws
rosinstall_generator ros_comm sensor_msgs --rosdistro melodic --deps --tar > melodic-ros_comm.rosinstall
wstool init -j8 src melodic-ros_comm.rosinstall
rosdep install --from-paths src --ignore-src --rosdistro melodic -y
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release
echo "source ~/ros_catkin_ws/install_isolated/setup.bash" >> ~/.bashrc
echo "export ROS_MASTER_URI=http://raspberrypi:11311/" >> ~/.bashrc

EOF

# COPY ROS APP AND SERVICE
