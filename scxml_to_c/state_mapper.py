from lxml import etree
from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow, VariableValue, AddressOf, TextModifier)





if __name__ == "__main__":
    state_map = Variable('map',
                         'state_t',
                         value=[{'Handler':1,
                                 'Entry':2,
                                 'Exit':3,
                                 'Parent':4,
                                 'Node': 5, 
                                 'Level': 1},
                                 {'Handler':1,
                                 'Entry':2,
                                 'Exit':3,
                                 'Parent':4,
                                 'Node': 5, 
                                 'Level': 1}])
    tree = etree.parse('simple.scxml')
    root = tree.getroot()
    list(root)

    # create states
    NULL = TextModifier("NULL")
    level = 0
    states = [state for state in list(root) if state.tag=='state']
    state_defititions = CodeWriter()
    for state in states:
        state_name = state.get('id')
        children = [child for child in list(state) if child.tag=='state']
        Node = TextModifier(f'&children_of_{state_name}') if children else NULL
        state_t = Variable(name=state_name,
                           primitive='state_t',
                           qualifiers=['static', 'const'],
                           value={'Handler': TextModifier(f'{state_name}_handler'),
                                  'Entry': TextModifier(f'{state_name}_entry'),
                                  'Exit': TextModifier(f'{state_name}_exit'),
                                  'Parent': NULL,
                                  'Node': Node,
                                  'Level': 0}
                                  )
        state_defititions.add_variable_initialization(state_t)
        state_defititions.add_line()

    print(state_defititions)

    # create an array for the next level