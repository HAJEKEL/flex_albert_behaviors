#!/usr/bin/env python
import actionlib
import rospy
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from order_package.msg import OrderGoal

from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import *
from geometry_msgs.msg import Pose, Quaternion
from tf import transformations
import tf_conversions

"""
Created on 11/19/2015

@author: Spyros Maniatopoulos
"""



class MoveBase(EventState):
    """
    Navigates the robot base to the position published on the current_order topic


    <= arrived                  Navigation to target pose succeeded.
    <= failed                   Navigation to target pose failed.
    <= customer_interaction     Customer interaction is required after arriving.
    """

    def __init__(self):
        """Constructor"""

        super(MoveBase, self).__init__(outcomes=['arrived', 'failed', 'customer_interaction'])

        self._action_topic = "/move_base"

        self._client = ProxyActionClient({self._action_topic: MoveBaseAction})

        self._arrived = False
        self._failed = False
        self._customer_interaction = False
        self._current_order_topic = '/order_node/current_order'

    def execute(self, userdata):
        """Wait for action result and return outcome accordingly"""

        if self._arrived:
            return 'arrived'
        if self._failed:
            return 'failed'

        # check on parameter server if customer interaction is required
        self._customer_interaction = rospy.get_param('/request_pending')
        

        if self._client.has_result(self._action_topic):
            status = self._client.get_state(self._action_topic)
            if status == GoalStatus.SUCCEEDED:
                self._arrived = True
                if self._customer_interaction:
                    return 'customer_interaction'
                else:
                    return 'arrived'

            elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
                            GoalStatus.RECALLED, GoalStatus.ABORTED]:
                Logger.logwarn('Navigation failed: %s' % str(status))
                self._failed = True
                return 'failed'

    def on_enter(self, userdata):

        self._arrived = False
        self._failed = False

        goal = MoveBaseGoal()

        # get current order from topic
        current_order = rospy.wait_for_message(self._current_order_topic, OrderGoal)

        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose = current_order.waypoint


        # Send the action goal for execution
        try:
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True

    def cancel_active_goals(self):
        if self._client.is_available(self._action_topic):
            if self._client.is_active(self._action_topic):
                if not self._client.has_result(self._action_topic):
                    self._client.cancel(self._action_topic)
                    Logger.loginfo('Cancelled move_base active action goal.')

    def on_exit(self):
        self.cancel_active_goals()

    def on_stop(self):
        self.cancel_active_goals()
