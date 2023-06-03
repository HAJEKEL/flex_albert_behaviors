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


class CustomerInteractionState(EventState):
	"""
	Navigates a robot to a desired position and orientation using move_base.

	># waypoint     Pose2D      Target waypoint for navigation.

	<= arrived                  Navigation to target pose succeeded.
	<= failed                   Navigation to target pose failed.
	"""

	def __init__(self):
		"""Constructor"""

		super(CustomerInteractionState, self).__init__(outcomes=['ordersent'])

		self._action_topic = "/customer_interaction_server"

		self._client = ProxyActionClient({self._action_topic: CustomerInteractionAction})
		rospy.wait_for_service('order_node/add_task')
		self.order_service = rospy.ServiceProxy('order_node/add_task', AddTask)
		self._ordersent = False
		self._failed = False
	def execute(self, userdata):
		"""Wait for action result and return outcome accordingly"""

		if self._ordersent:
			return 'ordersent'

		if self._client.has_result(self._action_topic):
			request = OrderRequest()
			result = self._client.get_result(self._action_topic)
			request.product_name = result.wanted_product
			request.order_id = 0
			if result.picking_assistance:
				request.request_type = 1
			else:
				request.request_type = 2

			rospy.loginfo("Sending order request...")
			self._ordersent = True
			response = self.order_service(request)
			#if response.success:
			#	rospy.loginfo("Order request succeeded")
			#	self._ordersent = True
			#else:
			#	rospy.loginfo("Order request failed")



			#elif status in [GoalStatus.PREEMPTED, GoalStatus.REJECTED,
			#                GoalStatus.RECALLED, GoalStatus.ABORTED]:
			#	Logger.logwarn('Navigation failed: %s' % str(status))
			#	self._failed = True
			#	return 'failed'

	def on_enter(self, userdata):

		self._ordersent = False
		self._failed = False
		#set goal
		goal = CustomerInteractionGoal()
		# Send the action goal for execution
		try:
			self._client.send_goal(self._action_topic, goal)
		except Exception as e:
			Logger.logwarn("unable to send goal:\n%s" % str(e))
			self._failed = True

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
