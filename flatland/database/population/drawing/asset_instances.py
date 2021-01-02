"""
asset_instances.py
"""

population = [
    # xuml class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawing type': 'xuml class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawing type': 'xuml class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawing type': 'xuml class diagram'},

    # Shlaer-Mellor class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawing type': 'Shlaer-Mellor class diagram'},

    # Starr class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'label', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'see also', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'class name', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'methods', 'Form': 'text', 'drawing type': 'Starr class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    # For diagnostics only
    {'Name': 'shoot', 'Form': 'shape', 'drawing type': 'Starr class diagram'},

    # Symbols
    {'Name': 'solid arrow', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'hollow arrow', 'Form': 'shape', 'drawing type': 'Starr class diagram'},
    {'Name': 'gen arrow', 'Form': 'shape', 'drawing type': 'Starr class diagram'},

    # xuml state machine diagram
    {'Name': 'transition', 'Form': 'shape', 'drawing type': 'xuml state machine diagram'},
    {'Name': 'event', 'Form': 'text', 'drawing type': 'xuml state machine diagram'},
    {'Name': 'activity', 'Form': 'text', 'drawing type': 'xuml state machine diagram'},
    {'Name': 'state name', 'Form': 'text', 'drawing type': 'xuml state machine diagram'},
    {'Name': 'state compartment', 'Form': 'shape', 'drawing type': 'xuml state machine diagram'},
    # Symbols
    {'Name': 'hollow large circle', 'Form': 'shape', 'drawing type': 'xuml state machine diagram'},
    {'Name': 'solid dot', 'Form': 'shape', 'drawing type': 'xuml state machine diagram'},

    # Domain diagram
    {'Name': 'domain node', 'Form': 'shape', 'drawing type': 'Starr domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'drawing type': 'Starr domain diagram'},

    {'Name': 'domain node', 'Form': 'shape', 'drawing type': 'xuml domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'drawing type': 'xuml domain diagram'},

    # Collaboration diagram
    {'Name': 'overview class', 'Form': 'shape', 'drawing type': 'Starr collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'drawing type': 'Starr collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'drawing type': 'Starr collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'drawing type': 'Starr collaboration diagram'},

    {'Name': 'overview class', 'Form': 'shape', 'drawing type': 'xuml collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'drawing type': 'xuml collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'drawing type': 'xuml collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'drawing type': 'xuml collaboration diagram'}
]