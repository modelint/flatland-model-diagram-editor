"""
compartment_type_instances.py
"""

population = [
    # Class diagram
    # Class
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 1},

    {'Name': 'attribute', 'Horizontal alignment': 'LEFT', 'Vertical alignment': 'TOP',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 2},

    {'Name': 'method', 'Horizontal alignment': 'LEFT', 'Vertical alignment': 'TOP',
     'Pad top': 5, 'Pad bottom': 4, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'class', 'Diagram type': 'class', 'Stack order': 3},

    # Imported class
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'imported class', 'Diagram type': 'class', 'Stack order': 1},

    {'Name': 'attribute', 'Horizontal alignment': 'LEFT', 'Vertical alignment': 'TOP',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'imported class', 'Diagram type': 'class', 'Stack order': 2},

    # State machine diagram
    # State
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 10, 'Pad left': 10, 'Pad right': 10, 'Text style': 'TITLE',
     'Node type': 'state', 'Diagram type': 'state machine', 'Stack order': 1},

    {'Name': 'name only', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 20, 'Pad bottom': 20, 'Pad left': 10, 'Pad right': 10, 'Text style': 'TITLE',
     'Node type': 'state', 'Diagram type': 'state machine', 'Stack order': 3},

    {'Name': 'activity', 'Horizontal alignment': 'LEFT', 'Vertical alignment': 'TOP',
     'Pad top': 4, 'Pad bottom': 10, 'Pad left': 5, 'Pad right': 5, 'Text style': 'BODY',
     'Node type': 'state', 'Diagram type': 'state machine', 'Stack order': 2},

    # Domain diagram
    # Domain
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'domain', 'Diagram type': 'domain', 'Stack order': 1},

    # Class collaboration diagram
    # External entity
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'external entity', 'Diagram type': 'class collaboration', 'Stack order': 1},

    # Overview class
    {'Name': 'name', 'Horizontal alignment': 'CENTER', 'Vertical alignment': 'CENTER',
     'Pad top': 5, 'Pad bottom': 5, 'Pad left': 5, 'Pad right': 5, 'Text style': 'TITLE',
     'Node type': 'overview class', 'Diagram type': 'class collaboration', 'Stack order': 2}
]