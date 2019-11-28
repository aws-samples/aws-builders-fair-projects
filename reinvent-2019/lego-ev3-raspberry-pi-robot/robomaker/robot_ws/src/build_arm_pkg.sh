#!/bin/bash

cd robot_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
colcon bundle

