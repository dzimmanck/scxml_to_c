
from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow, VariableValue, AddressOf)
from scxml_to_c.helpers import get_transitions, get_ancestors
from scxml_to_c.functions import switch_state, traverse_state
from csnake.cconstructs import generate_c_value_initializer


def build_state_handler(node, hierarchical=False):
    state_name = node.get('id')
    function_name = f'{state_name}_handler'

    p = Variable('pState', 'state_machine_t *', "const")
    handler_function = Function(name=function_name, 
                                return_type='state_machine_result_t', 
                                arguments=(p,))

    # create a list of transitions and unique events
    transitions = get_transitions(node)
    events = []
    for transition in transitions:
        event = transition.get('event')
        if event not in events:
            events.append(event)

    return_function = traverse_state if hierarchical else switch_state
    result = Variable('result', primitive='state_machine_result_t',)

    # next state logic
    code = CodeWriter()
    code.start_switch(Arrow(p, 'Event'))
    for event in events:
        code.add_switch_case(Variable(event.upper(), 'int'))

        # get all transitions associated with this event
        these_transitions = [transition for transition in transitions 
                                        if transition.get('event') == event]
        this_tansition = these_transitions[0]
        target = Variable(this_tansition.get('target'), 'state_machine_t')
        call = return_function.generate_call('pState', AddressOf(target))

        # check if there is logic associated with event
        cond = this_tansition.get('cond')
        if cond:
            cond_formatted = ' '.join(cond.split())
            code.add_line(f'if {cond_formatted};')
            code.indent()
            code.add_line(f'return {call};')
            code.dedent()
        else:
            code.add_line(f'return {call};')
            code.dedent()

        for this_tansition in these_transitions[1:]:

            # if previous transition was unconditional, not need for evaluating other transitions
            if not cond:
                break

            # update the target and function call for this transition
            target = Variable(this_tansition.get('target'), 'state_machine_t')
            call = return_function.generate_call('pState', AddressOf(target))

            cond = this_tansition.get('cond')
            if cond:
                cond_formatted = ' '.join(cond.split())
                code.add_line(f'else if {cond_formatted};')
                code.indent()
                code.add_line(f'return {call};')
                code.dedent()
            else:
                code.add_line(f'return {call};')
                code.dedent()

        # if all transitions are conditional, add an "EVENT_HANDLED" at the end for case where
        # non of the conditional logic was asserted but the event was handled nonetheless
        if cond:
            code.add_line(f'return EVENT_HANDLED;')
            code.dedent()

    code.add_switch_default()
    code.add_line(f'return EVENT_UN_HANDLED;')
    code.dedent()
    code.end_switch()

    handler_function.add_code(code)

    return handler_function


if __name__ == "__main__":
    tree = etree.parse('simple.scxml')
    root = tree.getroot()
    print(dir(root))
    all_states = [child for child in root.iter('state')]
    print(all_states)
    code = CodeWriter()
    for state in all_states:
        state_handler = build_state_handler(state, True)
        code.add_function_definition(state_handler)
        code.add_line()
    print(code)