#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
import rospy
import actionlib
from retail_store_skills.msg import ScanShelfAction, ScanShelfGoal
from flexbe_core.proxy import ProxyActionClient
from actionlib_msgs.msg import GoalStatus


class ScanShelfState(EventState):
    '''
    Example for a state to demonstrate which functionality is available for state implementation.
    This example lets the behavior wait until the given target_time has passed since the behavior has been started.

    -- target_time 	float 	Time which needs to have passed since the behavior started.

    <= continue 			Given time has passed.
    <= failed 				Example for a failure outcome.

    '''

    def __init__(self):

        super(ScanShelfState, self).__init__(outcomes=['scanned', 'failed'])
        self._action_topic = "/scan_shelf_server"
        self._client = ProxyActionClient({self._action_topic: ScanShelfAction})
        self._scanned = False
        self._failed = False

    def execute(self, userdata):
        if self._scanned:
            return 'scanned'
        if self._failed:
            return 'failed'
        if self._client.has_result(self._action_topic):
            self._scanned = True
            return 'scanned'

    # if self._client.has_result(self._action_topic):
    # 	status = self._client.get_state(self._action_topic)
    # 	if status == GoalStatus.SUCCEEDED:
    # 		self._scanned = True
    # 		return 'scanned'
    # 	elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
    # 		GoalStatus.RECALLED, GoalStatus.ABORTED]:
    # 		Logger.logwarn('failed to scan: %s' % str(status))
    # 		self._failed = True
    # 		return 'failed'

    def on_enter(self, userdata):

        self._scanned = False
        self._failed = False

        # Create and populate action goal
        goal = ScanShelfGoal()
        goal.shelf_direction = 0.0
        rospy.loginfo("Sending placing goal...")
        # Send the action goal for execution
        try:
            self._client.send_goal(self._action_topic, goal)
        except Exception as e:
            Logger.logwarn("Unable to send navigation action goal:\n%s" % str(e))
            self._failed = True

    def on_exit(self, userdata):
        # This method is called when an outcome is returned and another state gets active.
        # It can be used to stop possibly running processes started by on_enter.
        self.cancel_active_goals()

    # pass # Nothing to do in this example.

    def cancel_active_goals(self):
        if self._client.is_available(self._action_topic):
            if self._client.is_active(self._action_topic):
                if not self._client.has_result(self._action_topic):
                    self._client.cancel(self._action_topic)
                    Logger.loginfo('Cancelled move_base active action goal.')

    def on_stop(self):
        # This method is called whenever the behavior stops execution, also if it is cancelled.
        # Use this event to clean up things like claimed resources.
        self.cancel_active_goals()
# pass # Nothing to do in this example.
