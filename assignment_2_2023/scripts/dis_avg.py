#! /usr/bin/env python


"""

.. module: Node C, Distance and average speed

   :platform: Unix
   :synopsis: Service node which calculates and returns the distance of the robot from the target and the robot's average speed along x-axis (linear) and z-axis (angular)
 
.. moduleauthor:: Nicolas Bravi nicolasbravi2001@gmail.com
   
ROS node for getting the robot-target distance and its average speed.


Subscribes to:
   /status
Services:
   /dist_avg
Clients:
   /reaching_goal
   
"""





import rospy
from assignment_2_2023.msg import Status
from assignment_2_2023.srv import DisAvg, DisAvgResponse
import sys
import actionlib
import actionlib.msg
import math
from geometry_msgs.msg import Pose, Twist, Point
from nav_msgs.msg import Odometry
import time

# position and velocity list of the robot
global x,y,v_x_list, v_z_list
x=0
y=0
v_x_list = []
v_z_list = []



# callback function for the service
def distAvgCallback(msg):
    """
    Callback function for the service, it responses with the distance of the robot from the target and the robot's average speed along x-axis and z-axis.
    """
    
    # goal coordinates
    des_x=rospy.get_param('des_pos_x')
    des_y=rospy.get_param('des_pos_y')

    #distance from robot to goal
    distance = math.sqrt(pow(des_x-x,2) + pow(des_y-y,2))

    # average of speed along x-axis and z-axis
    avg_v_x=sum(v_x_list)/len(v_x_list) 
    avg_v_z=sum(v_z_list)/len(v_z_list)
    
    # response of the service request
    return DisAvgResponse(distance,avg_v_x,avg_v_z)




# callback function for the subscriber '/status'
def subCallback(msg):
    """
    Callback function of subscriber '/status', it updates the values of distance and speed.
    """


    global x,y
    
    x = msg.x
    y = msg.y
    v_x_list.append(msg.v_x)
    v_z_list.append(msg.v_z)

    # param set in assigment1.launch
    windowSize = rospy.get_param("/window_size")
    

    #In order to calculate the average, we take the "windowSize" new values
    if len(v_x_list) > windowSize:
        v_x_list.pop(0) # remove the first value (oldest)
        v_z_list.pop(0) # remove the first value (oldest)



    
def main():
    """
    This is the main code of the dis_avc service node.
    """
    # initialize the node dist_avg_srv
    rospy.init_node('dist_avg_srv')

    # subscriber '/status'
    rospy.Subscriber("/status", Status, subCallback)
    
    # define service dist_avg
    rospy.Service('dist_avg', DisAvg, distAvgCallback)
    
    # spin to hold this as a server
    rospy.spin()  
    



if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)



