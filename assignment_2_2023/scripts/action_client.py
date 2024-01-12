#! /usr/bin/env python


import rospy
from geometry_msgs.msg import Point, Pose, Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import actionlib
import actionlib.msg
import assignment_2_2023.msg
from assignment_2_2023.msg import Status
from tf import transformations
from std_srvs.srv import *
import time



#from __future__ import print_function


# Brings in the SimpleActionClient
#import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
#import actionlib_tutorials.msg


def callback(msg):
    status = Status();
    
    # set the parameters of the new message, with the data from the Odometry message
    status.x = msg.pose.pose.position.x
    status.y = msg.pose.pose.position.y
    status.v_x = msg.twist.twist.linear.x
    status.v_z = msg.twist.twist.angular.z
    # publish the new message on the topic /nicolas
    pub.publish(status)



def action_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    
    client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2023.msg.PlanningAction)

    # Waits until the action server has started up and started
    # listening for goals.
    
    client.wait_for_server()

    # Creates a goal to send to the action server.
    
    #if client.get_state() == actionlib.GoalStatus.SUCCEDED:
    #    rospy.loginfo("Goal reached")
    #    print("ho raggiunto")
            
    #else:
    #    command = input("Press c to cancel the goal, otherwhise press anything else: ")
    #    if command == 'c':
    #        client.cancel_goal()
    #        rospy.loginfo("Goal cancelled")
    #        print("ho cancellato")
        
    
         
    print("Insert a goal")
    
    x = float(input("Insert x: "))
    y = float(input("Insert y: "))
        
        
    goal = assignment_2_2023.msg.PlanningGoal()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
        
    rospy.set_param('des_pos_x', x)
    rospy.set_param('des_pos_y', y)
        
    client.send_goal(goal)
        
        
        

        
    
    
    
    
    
    
    # cancel goal    
    #print("\nPress 1 to cancel, other to continue")
    #x = float(input("Insert x: ")
    
    
def main():
    
    print("Aiuto bro")
    
    rospy.init_node('action_client_py')
    
    global pub
    pub = rospy.Publisher("/nicolas", Status, queue_size = 1)
    
    rospy.Subscriber("/odom", Odometry, callback)
    
    while not rospy.is_shutdown():
        print("Aiuto bro")
        action_client()
        rospy.spin()
    
    




if __name__ == '__main__':
    try:
        print("lancialoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        main()
        
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr) 
