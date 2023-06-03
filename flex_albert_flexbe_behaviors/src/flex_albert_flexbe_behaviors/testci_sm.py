#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_albert_flexbe_states.customer import CustomerInteractionState

# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jun 02 2023
@author: ernst
'''


class testCISM(Behavior):
    '''
    test customer interaction
    '''

    def __init__(self):
        super(testCISM, self).__init__()
        self.name = 'testCI'

    # parameters of this behavior

    # references to used behaviors

    # Additional initialization code can be added inside the following tags
    # [MANUAL_INIT]

    # [/MANUAL_INIT]

    # Behavior comments:

    def create(self):
        # x:30 y:365, x:130 y:365
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

        # [/MANUAL_CREATE]

        with _state_machine:
            # x:123 y:83
            OperatableStateMachine.add('test',
                                       CustomerInteractionState(),
                                       transitions={'ordersent': 'finished'},
                                       autonomy={'ordersent': Autonomy.Off})

        return _state_machine

# Private functions can be added inside the following tags
# [MANUAL_FUNC]

# [/MANUAL_FUNC]
