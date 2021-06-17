from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow)
from scxml_to_c.comments import (ENUM_DEC_LINES, 
                                 STRUCT_DEC_LINES, 
                                 EXTERNAL_FUN_PROTO_DEC_LINES, 
                                 INC_DEC_LINES, 
                                 FUN_PROTO_DEC_LINES, 
                                 GLOBAL_DEC_LINES, 
                                 FUN_DEC_LINES)
from scxml_to_c.state_mapper import generate_state_globals
import argparse
import scxml_to_c.helpers as helpers
from scxml_to_c.builders import build_function_prototype, build_state_handler
import sys
import os

def make_header(name, root):

    # create a list of all unique events
    transitions = root.findall('.//transition')
    events = []
    for transition in transitions:
        event = transition.get('event').upper()
        if event not in events:
            events.append(event)


    code = CodeWriter()
    code.add_autogen_comment()
    code.add_line()
    event_e = Enum(name="event_t",
                  typedef=True)

    # add the event enum
    event_e.add_value(events[0], 1)
    for event in events[1:]:
        event_e.add_value(event)
    code.add_lines(ENUM_DEC_LINES)
    code.add_line()
    code.add_enum(event_e)

    # add state machine struct
    strct  = Struct(f'{name}_state_machine_t', typedef=False)
    var1 = Variable("Machine", "state_machine_t")
    var2 = Variable("Dummy1", "uint32_t")   # FIXME: Make it not dumb
    var3 = Variable("Dummy2", "uint32_t")   # FIXME: Make it not dumb
    strct.add_variable(var1)
    strct.add_variable(var2)
    strct.add_variable(var3)
    code.add_lines(STRUCT_DEC_LINES)
    code.add_line()
    code.add_struct(strct)
    code.add_line()

    # external function prototype
    code.add_lines(EXTERNAL_FUN_PROTO_DEC_LINES)
    p = Variable(f'p{name}', f'{name}_state_machine_t *', "const")
    init_fun = Function(name=f'init_{name}',
                        arguments=(p,))
    code.add_function_prototype(init_fun, extern=True)

    return code

def make_source(name, root, hierarchical=False):
    code = CodeWriter()
    code.add_autogen_comment()
    code.add_line()

    # includes
    code.add_lines(INC_DEC_LINES)
    code.include("<stdint.h>")
    code.include("<stdio.h>")
    code.include("<stdbool.h>")
    code.add_line()
    code.include('"hsm.h"')
    code.include('"demo.h"')
    code.add_line()

    # find all of the states
    all_states = [child for child in root.iter('state')]

    # function prototype
    code.add_lines(FUN_PROTO_DEC_LINES)
    for state in all_states:
        state_function_prototype = build_function_prototype(state)
        code.add_lines(state_function_prototype)

    # global variables
    code.add_lines(GLOBAL_DEC_LINES)
    global_variables = generate_state_globals(root,  hierarchical)
    for variable in global_variables:
        code.add_variable_initialization(variable)
        code.add_line()

    # initialization function
    code.add_lines(FUN_DEC_LINES)
    p = Variable(f'p{name}', f'{name}_state_machine_t *', "const")
    init_fun = Function(name=f'init_{name}',
                        arguments=(p,))
    state = Arrow(p, 'Machine.State')
    event = Arrow(p, 'Machine.Event')
    initial_state = root.get('initial')
    fun_code = (f'{state} = &{initial_state}',
                 f'{event} = 0')
    init_fun.add_code(fun_code)
    code.add_function_definition(init_fun)

    # state function handlers
    for state in all_states:
        state_handler = build_state_handler(state, hierarchical)
        code.add_function_definition(state_handler)
        code.add_line()

    return code


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid target directory")


def convert():
    """Some useful docstring
    """


    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--scxml', action="store", help='SCXML source file', required=True)
    parser.add_argument('-o', '--output-filename', action="store", help='Name of output file', required=True)  #TODO:  Consider making this optional, as we can grab a default name from SCXML file
    parser.add_argument('-d', '--directory', action="store", help='Target directory for output files', type=dir_path, required=False)

    opts = parser.parse_args()
    scxml = opts.scxml
    name = opts.output_filename
    directory = opts.directory

    # passe the SCXML file
    tree = etree.parse(scxml)
    root = tree.getroot()

    # get the number of levels
    num_levels = helpers.find_num_levels(root) - 1  # subtract 1 because we don't count the root as a level
    hierarchical = num_levels > 1

    # generate code
    header = make_header(name, root)
    source = make_source(name, root, hierarchical)

    # output code to files
    if directory is None:
        header_path = os.path.abspath(f'{name}.h')
        src_path = os.path.abspath(f'{name}.c')
    else:
        header_path = os.path.abspath(f'{directory}/{name}.h')
        src_path = os.path.abspath(f'{directory}/{name}.c')
    header.write_to_file(header_path)
    source.write_to_file(src_path)


def _convert():
    try:
        sys.exit(convert())
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    _convert()