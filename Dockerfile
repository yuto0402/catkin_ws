FROM ros:noetic-ros-base-focal
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ros-noetic-turtlesim ros-noetic-turtlebot3-gazebo ros-noetic-turtlebot3-teleop \
    ros-noetic-gazebo-plugins ros-noetic-rqt-graph ros-noetic-robot-state-publisher \
    ros-noetic-rviz ros-noetic-rviz-imu-plugin \
    xvfb x11vnc novnc websockify openbox mesa-utils x11-utils \
    && rm -rf /var/lib/apt/lists/*
RUN sed -i '/<launch>/a\  <arg name="world_name" default="$(find turtlebot3_gazebo)/worlds/empty.world"/>' /opt/ros/noetic/share/turtlebot3_gazebo/launch/turtlebot3_empty_world.launch \
    && sed -i 's|value="$(find turtlebot3_gazebo)/worlds/empty.world"|value="$(arg world_name)"|' /opt/ros/noetic/share/turtlebot3_gazebo/launch/turtlebot3_empty_world.launch
