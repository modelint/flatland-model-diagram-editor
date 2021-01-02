"""
stem_type_instances.py
"""
population = [
    # Class diagram
    {'Name': 'class mult', 'Diagram type': 'class', 'connector type': 'binary association',
     'About': 'How many instances may be associated', 'Minimum length': 20, 'Geometry': 'fixed'},
    {'Name': 'associative mult', 'Diagram type': 'class', 'connector type': 'binary association',
     'About': 'How many association class instances per pair of associated instances', 'Minimum length': 24,
     'Geometry': 'hanging'},
    {'Name': 'superclass', 'Diagram type': 'class', 'connector type': 'generalization',
     'About': 'The superset of all subclass instances', 'Minimum length': 18, 'Geometry': 'fixed'},
    {'Name': 'subclass', 'Diagram type': 'class', 'connector type': 'generalization',
     'About': 'A disjoint subset of the superclass set of instances', 'Minimum length': 10, 'Geometry': 'fixed'},

    # State machine diagram
    {'Name': 'from state', 'Diagram type': 'state machine', 'connector type': 'transition',
     'About': 'Points to the source state in a transition', 'Minimum length': 10, 'Geometry': 'fixed'},
    {'Name': 'to state', 'Diagram type': 'state machine', 'connector type': 'transition',
     'About': 'Points to the destination state in a transition', 'Minimum length': 15, 'Geometry': 'fixed'},
    {'Name': 'to initial state', 'Diagram type': 'state machine', 'connector type': 'initial transition',
     'About': 'Points to a designated state as an initial state', 'Minimum length': 60, 'Geometry': 'free'},
    {'Name': 'from deletion state', 'Diagram type': 'state machine', 'connector type': 'deletion transition',
     'About': 'Points away from a final state to indicate deletion', 'Minimum length': 50, 'Geometry': 'free'},

    # Domain diagram
    {'Name': 'to service', 'Diagram type': 'domain', 'connector type': 'bridge', 'Geometry': 'fixed',
     'About': 'Points toward a domain that fullfills the requirements of a client domain', 'Minimum length': 15},
    {'Name': 'from service', 'Diagram type': 'domain', 'connector type': 'bridge', 'Geometry': 'fixed',
     'About': 'Points toward a domain that places requirements on a service domain', 'Minimum length': 15},

    # Collaboration diagram
    {'Name': 'on collaborator', 'Diagram type': 'class collaboration', 'connector type': 'collaboration',
     'About': 'Attaches to a communicating entity', 'Minimum length': 10, 'Geometry': 'fixed'}
]