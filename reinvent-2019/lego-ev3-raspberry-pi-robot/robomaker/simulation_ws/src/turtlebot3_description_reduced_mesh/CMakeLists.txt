cmake_minimum_required(VERSION 2.8.3)
project(turtlebot3_description_reduced_mesh)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
)

catkin_package(DEPENDS gazebo_ros)

install(DIRECTORY launch meshes urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

