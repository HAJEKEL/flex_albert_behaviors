#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_albert_flexbe_states.move2 import MoveBaseState2
from flex_albert_flexbe_states.ordermaster import OrderMasterState
from flex_albert_flexbe_states.pickproduct import PickProductState
from flex_albert_flexbe_states.placeproductbasket import PlaceProductBasketState
from flex_albert_flexbe_states.scanshelf import ScanShelfState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 01 2023
@author: Ernst
'''
class albert_FSMSM(Behavior):
	'''
	behavior for the albert robot to move to shelf and pick product
	'''


	def __init__(self):
		super(albert_FSMSM, self).__init__()
		self.name = 'albert_FSM'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]

    # [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:767 y:424, x:194 y:444
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.x = -2.5
		_state_machine.userdata.y = 2
		_state_machine.userdata.yaw = 3.14
		_state_machine.userdata.apriltag_id = 18
		_state_machine.userdata.waypoint = 0
		_state_machine.userdata.ordercomplete = 1
		_state_machine.userdata.request_type = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]

        # [/MANUAL_CREATE]


		with _state_machine:
			# x:186 y:31
			OperatableStateMachine.add('order master',
										OrderMasterState(),
										transitions={'userdatachanged': 'move base'},
										autonomy={'userdatachanged': Autonomy.Off},
										remapping={'waypoint': 'waypoint', 'apriltag_id': 'apriltag_id', 'ordercomplete': 'ordercomplete', 'request_type': 'request_type'})

			# x:466 y:261
			OperatableStateMachine.add('pick product',
										PickProductState(),
										transitions={'picked': 'place product', 'failed': 'failed'},
										autonomy={'picked': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'apriltag_id': 'apriltag_id'})

			# x:631 y:314
			OperatableStateMachine.add('place product',
										PlaceProductBasketState(),
										transitions={'placed': 'order master', 'failed': 'failed'},
										autonomy={'placed': Autonomy.Off, 'failed': Autonomy.Off})

			# x:309 y:225
			OperatableStateMachine.add('scan shelf',
										ScanShelfState(),
										transitions={'scanned': 'pick product', 'failed': 'failed'},
										autonomy={'scanned': Autonomy.Off, 'failed': Autonomy.Off})

			# x:140 y:138
			OperatableStateMachine.add('move base',
										MoveBaseState2(),
										transitions={'arrived': 'scan shelf', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'waypoint': 'waypoint'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]

# [/MANUAL_FUNC]
