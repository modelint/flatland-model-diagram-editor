"""
compartment_type_instances.py
"""

population = [
    # Class diagram
    # Class
    {'Name': 'class name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 1},

    {'Name': 'attributes', 'Horizontal alignment': 'LEFT',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 2},

    {'Name': 'methods', 'Horizontal alignment': 'LEFT',
     'Pad top': 5, 'Pad bottom': 4, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 3},

    # Imported class
    {'Name': 'class name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'imported class', 'Diagram type': 'class', 'Stack order': 1},

    {'Name': 'attributes', 'Horizontal alignment': 'LEFT',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'imported class', 'Diagram type': 'class', 'Stack order': 2},

    # State machine diagram
    # State
    {'Name': 'state name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'state', 'Diagram type': 'state machine', 'Stack order': 1},

    {'Name': 'activity', 'Horizontal alignment': 'LEFT',
     'Pad top': 4, 'Pad bottom': 4, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'state', 'Diagram type': 'state machine', 'Stack order': 2},

    # Domain diagram
    # Domain
    {'Name': 'domain name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'domain', 'Diagram type': 'domain', 'Stack order': 1},

    # Class collaboration diagram
    # External entity
    {'Name': 'entity name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'external entity', 'Diagram type': 'class collaboration', 'Stack order': 1},

    # Overview class
    {'Name': 'class name', 'Horizontal alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'overview class', 'Diagram type': 'class collaboration', 'Stack order': 2}
]