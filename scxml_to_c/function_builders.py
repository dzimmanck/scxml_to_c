
from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow)
from scxml_to_c.helpers import get_transitions

# typedefs
state_machine_result_t = "state_machine_result_t"


def build_state_handler(node):
    # get all node parents
    function_name = "1_2_3"

    p = Variable('pState', 'state_machine_t *', "const")
    handler_function = Function(name=function_name, 
                                return_type=state_machine_result_t, 
                                arguments=(p,))

    transitions = get_transitions(node)

    # next state logic
    code = CodeWriter()
    event = Arrow(p, 'Event')
    code.start_switch(event)
    for transition in transitions:
        code.add_switch_case(transition.get('event'))
        code.add_switch_return(f'traverse_state({p}, &Level3_HSM[0])')
    code.add_switch_default()
    code.add_switch_return('EVENT_UN_HANDLED')

    handler_function.add_code(code)

    return handler_function




if __name__ == "__main__":
    tree = etree.parse('simple.scxml')
    root = tree.getroot()

    leve1_states = root.getchildren()
    light = leve1_states[1]
    test_state = light.getchildren()[2]

    state_handler = build_state_handler(test_state)
    
    code = CodeWriter()
    code.add_function_definition(state_handler)
    print(code)