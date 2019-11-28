ARG ROS_VERSION=kinetic
ARG UBUNTU_VERSION=xenial
FROM arm32v7/ros:${ROS_VERSION}-ros-base-${UBUNTU_VERSION}

ENV PATH="/root/.local/bin:${PATH}"

# Copy qemu from the host machine
COPY qemu-arm-static /usr/bin

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Installed for convenience
RUN apt-get update && apt-get install -y vim

# Install Raspberry Pi package sources and libraries
RUN apt-get update && apt-get install -y gnupg lsb-release software-properties-common \
    && add-apt-repository -y ppa:ubuntu-pi-flavour-makers/ppa \
    && apt-get update && apt-get install -y libraspberrypi0

# Install Python and colcon
RUN apt-get update && apt-get install -y \
      python \
      python3-apt \
      curl \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && python2 get-pip.py \
    && python3 -m pip install -U colcon-ros-bundle

# Add custom rosdep rules
COPY robomaker/object-tracker.yaml /etc/ros/rosdep/custom-rules/object-tracker.yaml
RUN echo "yaml file:/etc/ros/rosdep/custom-rules/object-tracker.yaml" > /etc/ros/rosdep/sources.list.d/23-object-tracker-rules.list \
    && echo "yaml https://s3-us-west-2.amazonaws.com/rosdep/python.yaml" > /etc/ros/rosdep/sources.list.d/18-aws-python.list \
    && rosdep update

# Add custom pip rules
COPY robomaker/custom-pip-rules.conf   /etc/pip.conf

# Add custom apt sources for bundling
COPY robomaker/xenial-sources.yaml /opt/cross/apt-sources.yaml

