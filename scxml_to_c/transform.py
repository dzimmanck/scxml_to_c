from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow)
from comments import ENUM_DEC_LINES, STRUCT_DEC_LINES, INC_DEC_LINES, FUN_PROTO_DEC_LINES, GLOBAL_DEC_LINES, FUN_DEC_LINES


def get_states(node, prefix=''):
    """
    Recursion baby
    """
    states = []

    id  = node.get('id')

    if id:
        if prefix:
            prefix = f'{prefix}_{id}'
        else:
            prefix = id

    for state in node.iterchildren():
        states.extend(get_states(state, prefix=prefix))

    if not id:
        return states

    if not states:
        return [prefix]

    return states

class StateMachine():
    """Some useful docstring
    """

    def __init__(self, path, name='sm'):
        tree = etree.parse(path)
        root = tree.getroot()

        self.name = name

        self.num_levels = 3  # FIXME:  Need code for this
        self.hierarchical =  self.num_levels > 1

        # get the events
        transitions = root.findall('.//transition')
        events = []
        for transition in transitions:
            event = transition.get('event').upper()
            if event not in events:
                events.append(event)
        self.events = events

        self.states = get_states(root)

    def make_header(self):
        header = CodeWriter()
        header.add_autogen_comment()
        header.add_line()
        event_e = Enum(name="event_t",
                      typedef=True)

        # add the event enum
        event_e.add_value(self.events[0], 1)
        for event in self.events[1:]:
            event_e.add_value(event)
        header.add_lines(ENUM_DEC_LINES)
        header.add_line()
        header.add_enum(event_e)

        # add state machine struct
        strct  = Struct(f'{self.name}_state_machine_t', typedef=False)
        var1 = Variable("Machine", "state_machine_t")
        var2 = Variable("Dummy1", "uint32_t")   # FIXME
        var3 = Variable("Dummy2", "uint32_t")   # FIXME
        strct.add_variable(var1)
        strct.add_variable(var2)
        strct.add_variable(var3)
        header.add_lines(STRUCT_DEC_LINES)
        header.add_line()
        header.add_struct(strct)

        return header

    def make_source(self):

        src = CodeWriter()
        src.add_autogen_comment()
        src.add_line()

        # includes
        src.add_lines(INC_DEC_LINES)
        src.include("<stdint.h>")
        src.include("<stdio.h>")
        src.include("<stdbool.h>")
        src.add_line()
        src.add_line('"hsm.h"')
        src.add_line('"demo.h"')
        src.add_line()

        # function prototype
        src.add_lines(FUN_PROTO_DEC_LINES)
        var = Variable("const", "state_machine_t *")
        for state in self.states:
            fun = Function(name=f'{state}_handler', 
                            qualifiers="static",
                            return_type="state_machine_result_t", 
                            arguments=(var,))
            src.add_function_prototype(fun)
            fun = Function(name=f'{state}_entry_handler', 
                            qualifiers="static",
                            return_type="state_machine_result_t", 
                            arguments=(var,))
            src.add_function_prototype(fun)
            fun = Function(name=f'{state}_exit_handler', 
                            qualifiers="static",
                            return_type="state_machine_result_t", 
                            arguments=(var,))
            src.add_function_prototype(fun)
            src.add_line()

        # global variables
        src.add_lines(GLOBAL_DEC_LINES)
        
        src.add_line()

        # functions
        src.add_lines(FUN_DEC_LINES)
        p = Variable(f'p{self.name}', f'{self.name}_state_machine_t *', "const")
        init_fun = Function(name=f'init_{self.name}', 
                            return_type="void", 
                            arguments=(var,))
        state = Arrow(p, 'Machine.State')
        event = Arrow(p, 'Machine.Event')
        code = (f'{state} = &Level1_HSM[0]',
                f'{event} = 0')
        init_fun.add_code(code)
        src.add_function_definition(init_fun)

        

        return src








if __name__ == "__main__":
    # do something
    machine = StateMachine("simple.scxml", "inverter")
    # print(machine.make_header())
    print(machine.make_source())


# //! Simple hierarchical state machine
# typedef struct
# {
#   state_machine_t Machine;  //!< Abstract state machine
#   uint32_t Dummy1;          //!< Dummy variable
#   uint32_t Dummy2;          //!< Dummy variable
# }demo_state_machine_t;


