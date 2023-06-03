#!/usr/bin/env python
import actionlib
import rospy
import sys

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyActionClient
from actionlib_msgs.msg import GoalStatus
from voice_requests.msg import CustomerInteractionAction, CustomerInteractionGoal
from order_package.srv import AddTask
from order_package.msg import OrderRequest

#get current order from topic, change into userdata
class OrderMasterState(EventState):

	#retrieves latest order list, sends as userdata to other flexbe states

	def __init__(self):
		"""Constructor"""

		super(OrderMasterState, self).__init__(outcomes=['userdatachanged'],
		                                               input_keys['x', 'y', 'yaw','apriltag_id','ordercomplete','request_type'])

		self._sub = rospy.Subscriber('/order_node/order_list', String, self.callback)
		self._sub = rospy.Subscriber('/order_node/current_order.waypoint', String, self.callback)

		self._userdatachanged = False
		self._failed = False
	def execute(self, userdata):

		#get complete order list from somewhere

		if userdata.ordercomplete == 1: #order_complete is 1 if it is coming from place state
			#remove current order id from order list total, send that it is complete

			userdata.ordercomplete = 0


		if self._userdatachanged:
			return 'userdatachanged'

		userdata.request_type = 0
		userdata.x  = current_order.waypoint[1]
		userdata.y  = current_order.waypoint[2]
		userdata.yaw= current_order.waypoint[3]
		userdata.apriltag_id = order_list[3]

		self._userdatachanged = True

	def on_enter(self, userdata):

		self._userdatachanged = False
		self._failed = False




	#def cancel_active_goals(self):
	#	if self._client.is_available(self._action_topic):
	#		if self._client.is_active(self._action_topic):
	#			if not self._client.has_result(self._action_topic):
	#				self._client.cancel(self._action_topic)
	#				Logger.loginfo('Cancelled move_base active action goal.')

	#def on_exit(self, userdata):
	#self.cancel_active_goals()


	#def on_stop(self):
	#self.cancel_active_goals()