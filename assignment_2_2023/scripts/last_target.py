#! /usr/bin/env python
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.srv import LastInput, LastInputResponse


# callback of service last_input
def callback(msg):
    # get x,y goal from ROS parameter 
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    
    # response of the service request
    return LastInputResponse(x,y)


def main():
    # initialize node last_input_srv
    rospy.init_node('last_input_srv')

    # define service last_input
    rospy.Service('last_input', LastInput, callback)
    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)
