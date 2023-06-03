#!/usr/bin/env python
import actionlib
import rospy
import sys

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from actionlib_msgs.msg import GoalStatus
from voice_requests.msg import CustomerInteractionAction, CustomerInteractionGoal
from order_package.srv import AddTask
from order_package.msg import OrderGoal, OrderRequest
from std_srvs.srv import Trigger, TriggerResponse


# get current order from topic, change into userdata
class OrderMasterState(EventState):

    # retrieves latest order list, sends as userdata to other flexbe states

    def __init__(self):
        """Constructor"""

        super(OrderMasterState, self).__init__(outcomes=['userdatachanged'],
                                               input_keys=['waypoint', 'apriltag_id', 'ordercomplete', 'request_type'])

        # subscribe to current order topic
        rospy.wait_for_service('/order_node/mark_completed')
        self._markcompleted_srv = rospy.ServiceProxy('/order_node/mark_completed', Trigger)
        self._userdatachanged = False
        self._failed = False

    def execute(self, userdata):

        # get current order list from topic
        order_list = rospy.wait_for_message('/order_node/current_order', OrderRequest)
        userdata.waypoint = order_list.waypoint
        userdata.apriltag_id = order_list.apriltag_ids[0]
        userdata.request_type = order_list.request_type



        # get complete order list from somewhere
        self._markcompleted_srv(Trigger)

        if userdata.ordercomplete == 1:  # order_complete is 1 if it is coming from place state
            # remove current order id from order list total, send that it is complete
            # rosservice
            self.markcompleted_srv(Trigger)
            userdata.ordercomplete = 0

        if self._userdatachanged:
            return 'userdatachanged'

        self._userdatachanged = True

    def on_enter(self, userdata):

        self._userdatachanged = False
        self._failed = False



