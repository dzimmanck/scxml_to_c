
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow)



state = Variable('pState_Machine', 'state_machine_t *', "const")
target = Variable('pTarget_State', 'state_machine_t *', "const")
switch_state = Function(name='switch_state', 
                          return_type="state_machine_result_t", 
                          arguments=(state, target))
traverse_state = Function(name='traverse_state', 
                          return_type="state_machine_result_t", 
                          arguments=(state, target))