from csnake import TextModifier

NULL = TextModifier("NULL")

def has_entry(state):
    return state.find('onentry') is not None

def has_exit(state):
    return state.find('onexit') is not None

def get_parent_state(state):
    parent_element = state.getparent()
    if parent_element is not None:
        return parent_element.get('id')

def get_child_states(state):
    return [element for element in list(state) if element.tag=='state']

def get_transitions(state):
    return [element for element in list(state) if element.tag=='transition']


def get_ancestors(state):
    return [ancestor.get('id') for ancestor in state.iterancestors('state')]


def find_num_levels(state):
    levels = 1
    children = get_child_states(state)

    if not children:
        return levels
    levels += max([find_num_levels(child) for child in children])

    return levels

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



if __name__ == "__main__":
    from lxml import etree
    tree = etree.parse('simple.scxml')
    root = tree.getroot()
    print(find_num_levels(root))