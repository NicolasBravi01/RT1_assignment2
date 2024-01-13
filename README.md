 # Research Track 1, Assignment 2
Second assignment of Research Track 1 course at UniGe Robotics Engineering.

## Introduction
This project entails the development of three ROS (Robot Operating System) nodes to effectively maneuver a robot in a simulated 3D environment. The main node is designed for user interaction, allowing the specification and cancellation of target coordinates for the robot. One other node is dedicated to showing the coordinates of the last target sent by the user. The other node has to calculate and report the distance of the robot from its target and its average speed. We used Rviz and Gazebo for the simulation.

### Simulator
For this assignment, it was used Gazebo and Rviz within ROS. Gazebo served as the 3D simulation environment to test and refine the robot's movements, while Rviz was used for detailed 3D visualization, with also the information of the robot's sensor.

## Installing and running
First of all, you need to install xterm for the terminal interface
```bash
sudo apt-get install xterm
```

Then, clone the repository to your machine (or download)
```bash
git clone https://github.com/NicolasBravi01/RT1_assignment2.git
```
Before running, make the python files in the 'scripts' folder executable
```bash
cd scripts
chmod +x *.py
```

Now it is possible to run
```bash
roslaunch assignment_2_2023 assignment1.launch
```


## Nodes description
We just have provided theese nodes:
  - `bug_as.py`: Action server which implements the bug0 algorithm.
  - `wall_follow_service.py `: Service node that makes the robot follow the wall if it meets an obstacle.
  - `go_to_point_service.py `: Service node that makes the robot go straight to the goal position.

### action_client.py

### last_target.py

### dis_avg.py
