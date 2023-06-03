#!/usr/bin/env python
import actionlib
import rospy
import sys

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from actionlib_msgs.msg import GoalStatus
from std_srvs.srv import Trigger


# get current order from topic, change into userdata
class CompleteOrderState(EventState):
    '''
    This example lets the behavior wait until the given target_time has passed since the behavior has been started.


    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''
    # retrieves latest order list, sends as userdata to other flexbe states

    def __init__(self):
        """Constructor"""
        

        super(CompleteOrderState, self).__init__(outcomes=['complete'])

        # subscribe to current order topic
        rospy.wait_for_service('/order_node/mark_completed')
        self._markcompleted_srv = rospy.ServiceProxy('/order_node/mark_completed', Trigger)
        self._failed = False

    def execute(self, userdata):

        # send a trigger to the order node
        try:
            self._markcompleted_srv(Trigger)
            return 'continue'
        except:
            return 'failed'




