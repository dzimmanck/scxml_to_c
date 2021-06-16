from csnake import (CodeWriter, Enum, Struct, Variable, Function, Arrow, VariableValue, AddressOf)

def get_transitions(state):
    return [element for element in state.getchildren() if element.tag=='transition']


def get_ancestors(state):
    return [ancestor.get('id') for ancestor in state.iterancestors('state')]