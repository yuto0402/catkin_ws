source /opt/ros/noetic/setup.bash
source /home/student/catkin_ws/devel/setup.bash
export PATH="/home/student/catkin_ws/.ros-local/root/opt/ros/noetic/bin:$PATH"
export PYTHONPATH="/home/student/catkin_ws/.ros-local/root/opt/ros/noetic/lib/python3/dist-packages${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="/home/student/catkin_ws/.ros-local/root/opt/ros/noetic/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export ROS_PACKAGE_PATH="/home/student/catkin_ws/src:/home/student/catkin_ws/.ros-local/root/opt/ros/noetic/share:$ROS_PACKAGE_PATH"
export CMAKE_PREFIX_PATH="/home/student/catkin_ws/.ros-local/root/opt/ros/noetic:$CMAKE_PREFIX_PATH"
export ROS_HOME="/home/student/catkin_ws/.ros-local/runtime"
if [ -d /home/student/catkin_ws/.sim_deps/opt/ros/noetic ]; then
  export CMAKE_PREFIX_PATH="/home/student/catkin_ws/.sim_deps/opt/ros/noetic:$CMAKE_PREFIX_PATH"
  export PYTHONPATH="/home/student/catkin_ws/.sim_deps/opt/ros/noetic/lib/python3/dist-packages:$PYTHONPATH"
  export ROS_PACKAGE_PATH="/home/student/catkin_ws/.sim_deps/opt/ros/noetic/share:$ROS_PACKAGE_PATH"
  export LD_LIBRARY_PATH="/home/student/catkin_ws/.sim_deps/opt/ros/noetic/lib:$LD_LIBRARY_PATH"
  export GAZEBO_PLUGIN_PATH="/home/student/catkin_ws/.sim_deps/opt/ros/noetic/lib${GAZEBO_PLUGIN_PATH:+:$GAZEBO_PLUGIN_PATH}"
  export TURTLEBOT3_MODEL="${TURTLEBOT3_MODEL:-burger}"
fi
if [ -d /home/student/catkin_ws/.sim_deps/turtlebot3_simulations ]; then
  export ROS_PACKAGE_PATH="/home/student/catkin_ws/.sim_deps/turtlebot3_simulations:$ROS_PACKAGE_PATH"
fi
