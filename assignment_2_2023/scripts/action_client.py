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

def callback(msg):
    status = Status()
    status.x = msg.pose.pose.position.x
    status.y = msg.pose.pose.position.y
    status.v_x = msg.twist.twist.linear.x
    status.v_z = msg.twist.twist.angular.z
    pub.publish(status)

def action_client():
    
    goal_reached = True

    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)
    client.wait_for_server()

    while not rospy.is_shutdown():
        
        print("Insert 'c' to cancel the current goal, anything else to set a goal:")
        command = input("Enter command: ")  

        if command == 'c':
            if goal_reached == True:
                print("You have just reached the goal")
            else:
                client.cancel_goal()
                rospy.loginfo("Goal cancelled")
                continue

        limit = 10
        
        try:    
            x = float(input("Insert x: "))
            y = float(input("Insert y: "))
            
            if x<-limit or x>limit or y<-limit or y>limit:
                raise Exception(f"Insert values between [{-limit}, {limit}]")
                        
            goal_reached = False
        except ValueError:
            rospy.loginfo("Invalid input")
            continue
        except Exception as e:
            rospy.loginfo(e)
            continue
        

        goal = assignment_2_2023.msg.PlanningGoal()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        rospy.set_param('des_pos_x', x)
        rospy.set_param('des_pos_y', y)

        client.send_goal(goal)

        if client.get_state() == actionlib.GoalStatus.SUCCEEDED and goal_reached==False:
            rospy.loginfo("Goal reached")
            goal_reached = True
            

def main():
    
    rospy.init_node('action_client')
    global pub
    pub = rospy.Publisher("/status", Status, queue_size=1)
    rospy.Subscriber("/odom", Odometry, callback)
    
    action_client()
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print("Program interrupted before completion")
