echo "Setting up ROS..."
source /home/robot/ros_catkin_ws/install_isolated/setup.bash
export ROS_MASTER_URI=http://raspberrypi:11311/

while true
do
  /home/robot/controller.py
done
