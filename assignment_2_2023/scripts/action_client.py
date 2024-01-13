#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import actionlib
import assignment_2_2023.msg
from assignment_2_2023.msg import Status
from tf import transformations
from std_srvs.srv import *
import time
from actionlib_msgs.msg import GoalStatus


# Callback of subscriber '/odom', custom message 'Status' is used as a publisher
def callback(msg):
    status = Status()
    status.x = msg.pose.pose.position.x
    status.y = msg.pose.pose.position.y
    status.v_x = msg.twist.twist.linear.x
    status.v_z = msg.twist.twist.angular.z
    pub.publish(status)


# return true if the goal has been reached by the robot, false otherwise
def goalReached():
    return client.get_state() == actionlib.GoalStatus.SUCCEEDED

    




def action_client():
    
    # define action client
    global client
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)

    client.wait_for_server()

    while not rospy.is_shutdown():
        
        print("Insert 'c' to cancel the current goal, anything else to set a goal:")
        command = input("Enter command: ")  

        if command == 'c':
            # if the goal is reached, you can't cancel it
            if goalReached():
                print("You have just reached the goal, you cannot cancel it")
            else:
                # cancel the goal
                client.cancel_goal()
                rospy.loginfo("Goal cancelled")
                
            continue
        
        
        limit = 10
        
        # try to set the goal position
        try:    
            x = float(input("Insert x: "))
            y = float(input("Insert y: "))
            
            # x and y must be in the interval [-limit, limit], otherwise an exception is generated
            if x<-limit or x>limit or y<-limit or y>limit:
                raise Exception(f"Insert values between [{-limit}, {limit}]")
                        
        except ValueError:
            rospy.loginfo("Invalid input")
            continue

        except Exception as e:
            rospy.loginfo(e)
            continue
        
        # instance of the goal
        goal = assignment_2_2023.msg.PlanningGoal()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y

        # set x,y as ROS parameters
        rospy.set_param('des_pos_x', x)
        rospy.set_param('des_pos_y', y)

        # send the goal
        client.send_goal(goal)

            

def main():
    # initialize node action_client
    rospy.init_node('action_client')

    # define publisher '/status/
    global pub
    pub = rospy.Publisher("/status", Status, queue_size=1)

    # subscriber odom
    rospy.Subscriber("/odom", Odometry, callback)
    
    action_client()
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion")
