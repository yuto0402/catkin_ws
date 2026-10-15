#!/usr/bin/env bash
set -e
export DISPLAY=:99
export LIBGL_ALWAYS_SOFTWARE=1
export QT_X11_NO_MITSHM=1
unset LIBGL_ALWAYS_INDIRECT
if ! pgrep -x Xvfb >/dev/null; then
  rm -f /tmp/.X99-lock /tmp/.X11-unix/X99
fi
Xvfb :99 -screen 0 1280x800x24 -nolisten tcp &
for attempt in $(seq 1 50); do
  if glxinfo -B >/dev/null 2>&1; then break; fi
  sleep 0.1
done
if ! glxinfo -B >/dev/null 2>&1; then
  echo "Virtual display failed to start" >&2
  exit 1
fi
openbox >/tmp/openbox.log 2>&1 &
x11vnc -display :99 -localhost -rfbport 5900 -nopw -forever -shared >/tmp/x11vnc.log 2>&1 &
websockify --web=/usr/share/novnc 6080 localhost:5900 >/tmp/novnc.log 2>&1 &
source /opt/ros/noetic/setup.bash
if [ -f /catkin_ws/devel/setup.bash ]; then source /catkin_ws/devel/setup.bash; fi
export TURTLEBOT3_MODEL=burger
# 配布版で固定されている world_name を外から指定できるようにします。
tb3_launch=/opt/ros/noetic/share/turtlebot3_gazebo/launch/turtlebot3_empty_world.launch
if ! grep -q '<arg name="world_name" default=' "$tb3_launch"; then
  sed -i '/<launch>/a\  <arg name="world_name" default="$(find turtlebot3_gazebo)/worlds/empty.world"/>' "$tb3_launch"
  sed -i 's|value="$(find turtlebot3_gazebo)/worlds/empty.world"|value="$(arg world_name)"|' "$tb3_launch"
fi
# Gazebo はターミナルから必要な launch ファイルを一度だけ起動します。
exec roscore
