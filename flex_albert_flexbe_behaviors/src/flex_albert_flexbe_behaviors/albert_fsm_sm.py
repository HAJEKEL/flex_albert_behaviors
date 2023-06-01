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
		# x:819 y:412, x:145 y:433
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.x = -2.5
		_state_machine.userdata.y = 2
		_state_machine.userdata.yaw = 3.14
		_state_machine.userdata.apriltag_id = 18

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('move base',
										MoveBaseState2(),
										transitions={'arrived': 'scan shelf', 'failed': 'failed'},
										autonomy={'arrived': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'x': 'x', 'y': 'y', 'yaw': 'yaw'})

			# x:367 y:172
			OperatableStateMachine.add('pick product',
										PickProductState(),
										transitions={'picked': 'place product in basket', 'failed': 'failed'},
										autonomy={'picked': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'apriltag_id': 'apriltag_id'})

			# x:549 y:275
			OperatableStateMachine.add('place product in basket',
										PlaceProductBasketState(),
										transitions={'placed': 'finished', 'failed': 'failed'},
										autonomy={'placed': Autonomy.Off, 'failed': Autonomy.Off})

			# x:210 y:86
			OperatableStateMachine.add('scan shelf',
										ScanShelfState(),
										transitions={'scanned': 'pick product', 'failed': 'failed'},
										autonomy={'scanned': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
