#! /usr/bin/env python
import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.srv import LastInput, LastInputResponse



def callback(msg):
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    
    return LastInputResponse(x,y)


def main():
    rospy.init_node('last_input_srv')
    rospy.Service('last_input_srv', LastInput, callback)
    rospy.spin()


if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        # if the program is interrupted before completion, print a message
        print("Program interrupted before completion", file=sys.stderr)
