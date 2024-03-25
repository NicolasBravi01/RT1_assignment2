#! /usr/bin/env python

"""

.. module: Node B, Last Target

   :platform: Unix
   :synopsis: Service node which returns the coordinates of the last target sent by the user through the action_client node 
 
.. moduleauthor:: Nicolas Bravi nicolasbravi2001@gmail.com
   
ROS node for getting the last target assigned to the robot


Services:
   /last_input
Clients:
   /reaching_goal
   
"""



import rospy
import actionlib
import actionlib.msg
import assignment_2_2023.srv
import assignment_2_2023.msg
from assignment_2_2023.srv import LastInput, LastInputResponse


# callback of service last_input
def callback(msg):
    """
	Callback function of service last_input, which returns the last target coordinates
	
	Args:
	msg(PlanningActionGoal): robot's current goal
	"""
    # get x,y goal from ROS parameter 
    x=rospy.get_param('des_pos_x')
    y=rospy.get_param('des_pos_y')
    
    # response of the service request
    return LastInputResponse(x,y)


def main():
    """
    This is the main code of the last_target service node.
    """
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
