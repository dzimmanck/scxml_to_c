from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow, VariableValue, AddressOf, TextModifier)
from scxml_to_c.helpers import get_child_states
from scxml_to_c.builders import build_state_variable
NULL = TextModifier("NULL")

def add_finite_state_definition(state, state_defititions):
    state_name = state.get('id')
    state_t = build_state_variable(state)
    state_defititions.append(state_t)

# recursive function for generating state definition and child arrays
def add_hierarchical_state_definition(state, state_defititions, child_arrays, level=0, parent=None):
    state_name = state.get('id')
    children = get_child_states(state)
    Parent = TextModifier(f'&{parent}') if parent else NULL
    Node = TextModifier(f'&children_of_{state_name}') if children else NULL
    state_t = build_state_variable(state, level)

    for child in children:
        # create a definition for each child of this state as well
        add_hierarchical_state_definition(child, state_defititions, child_arrays, level+1, state_name)

    if children:
        # we also need to create an array of children for the Node attribute
        children_t = Variable(name=f'children_of_{state_name}',
                              primitive='state_t',
                              qualifiers = ['static', 'constant'],
                              value=[TextModifier(child.get('id')) for child in children])

        child_arrays.append(children_t)
    state_defititions.append(state_t)


def generate_state_globals(root, hierarchical=False):
    states = [state for state in list(root) if state.tag=='state']
    state_defititions = []

    if not hierarchical:
        for state in states:
            add_finite_state_definition(state, state_defititions)
        return state_defititions

    child_arrays = []
    for state in states:
        add_hierarchical_state_definition(state, state_defititions, child_arrays)

    return state_defititions + child_arrays


if __name__ == "__main__":

    tree = etree.parse('simple.scxml')
    definitions = generate_state_globals(tree)
    code = CodeWriter()
    for definition in definitions:
        code.add_variable_initialization(definition)
    print(code)
