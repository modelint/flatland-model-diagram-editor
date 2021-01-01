"""
node_type_instances.py
"""
population = [
    {'Name': 'class', 'About': 'Abstraction of a bunch of things with the same properies, ' +
                               'behavior and subject to same constraints and policies',
     'Corner rounding': 0, 'Border': 'Normal',
     'Default height': 80, 'Default width': 110, 'Max height': 180, 'Max width': 144, 'Diagram type': 'class'},

    {'Name': 'imported class', 'About': 'Used when you have a relationship to a class ' +
                                        'in some other subsystem of your domain.',
     'Corner rounding': 0, 'Border': 'Dashed',
     'Default height': 80, 'Default width': 110, 'Max height': 180, 'Max width': 144, 'Diagram type': 'class'},

    {'Name': 'state', 'About': "A context of some duration during an instance's existence",
     'Corner rounding': 4, 'Border': 'Normal',
     'Default height': 50, 'Default width': 110, 'Max height': 108, 'Max width': 300, 'Diagram type': 'state machine'},

    {'Name': 'overview class', 'About': 'Used to represent class in a collaboration or other non-class diagram',
     'Corner rounding': 0, 'Border': 'Normal',
     'Default height': 25, 'Default width': 100, 'Max height': 60, 'Max width': 300,
     'Diagram type': 'class collaboration'},

    {'Name': 'external entity', 'About': 'Proxy for an external domain or some aspect of an external domain',
     'Corner rounding': 0, 'Border': 'Normal',
     'Default height': 25, 'Default width': 100, 'Max height': 60, 'Max width': 300,
     'Diagram type': 'class collaboration'},

    {'Name': 'domain', 'About': 'A distinct subject matter with its own vocabulary and rules, ' +
                                'like "Linear Algebra" or "Configuration Management"',
     'Corner rounding': 0, 'Border': 'Normal',
     'Default height': 60, 'Default width': 100, 'Max height': 110, 'Max width': 300,
     'Diagram type': 'domain'},
]
