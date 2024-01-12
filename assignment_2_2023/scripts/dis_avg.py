#! /usr/bin/env python

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


global x,y,v_x_list, v_z_list
x=0
y=0
v_x_list = []
v_z_list = []



# callback function for the service
def distAvgCallback(msg):
    
    des_x=rospy.get_param('des_pos_x')
    des_y=rospy.get_param('des_pos_y')

    distance = math.sqrt(pow(des_x-x,2) + pow(des_y-y,2))

    avg_v_x=sum(v_x_list)/len(v_x_list) 
    avg_v_z=sum(v_z_list)/len(v_z_list)
    print(v_x_list)
    
    return DisAvgResponse(distance,avg_v_x,avg_v_z)




# callback function for the subscriber
def subCallback(msg):

    global x,y
    
    x = msg.x
    y = msg.y
    v_x_list.append(msg.v_x)
    v_z_list.append(msg.v_z)

    windowSize = 10

    #In order to calculate the average, we take the "windowSize" new values
    if len(v_x_list) > windowSize:
        v_x_list.pop(0) # remove the first value (oldest)
        v_z_list.pop(0) # remove the first value (oldest)



    
def main():
    rospy.init_node('dist_avg_srv')
    rospy.Subscriber("/status", Status, subCallback)
    rospy.Service('dist_avg', DisAvg, distAvgCallback)
    rospy.spin()  
    



if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)



