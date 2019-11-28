################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(object_tracker_robot)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(
  catkin REQUIRED COMPONENTS
)

################################################################################
# Declare ROS messages, services and actions
################################################################################

################################################################################
# Declare ROS dynamic reconfigure parameters
################################################################################

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  CATKIN_DEPENDS
)

################################################################################
# Build
################################################################################
include_directories(
  ${catkin_INCLUDE_DIRS}
)

################################################################################
# Install
################################################################################
add_custom_target(
  download_model ALL
  COMMAND python
  ${CMAKE_CURRENT_SOURCE_DIR}/scripts/download_model.py
  ${CMAKE_CURRENT_SOURCE_DIR}/config/model_config.yaml
  ${CMAKE_INSTALL_PREFIX}/${CATKIN_PACKAGE_SHARE_DESTINATION}/model.pb
)

install(PROGRAMS
  scripts/run_turtlebot_controller.sh
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
 DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

################################################################################
# Test
################################################################################
