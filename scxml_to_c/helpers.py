def get_transitions(state):
    return [element for element in state.getchildren() if element.tag=='transition']