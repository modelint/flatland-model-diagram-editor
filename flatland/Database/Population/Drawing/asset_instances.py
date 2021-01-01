"""
asset_instances.py
"""

population = [
    # xUML class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'label', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'see also', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'class name', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'methods', 'Form': 'text', 'Drawing type': 'xUML class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'Drawing type': 'xUML class diagram'},

    # Shlaer-Mellor class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'label', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'see also', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'class name', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'methods', 'Form': 'text', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'Drawing type': 'Shlaer-Mellor class diagram'},

    # Starr class diagram
    {'Name': 'class compartment', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'binary association connector', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'generalization connector', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'label', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'binary association name', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'generalization name', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'class mult name', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'imported class compartment', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'see also', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'class name', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'attributes', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'methods', 'Form': 'text', 'Drawing type': 'Starr class diagram'},
    {'Name': 'associative mult stem', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'grid', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'margin', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    # For diagnostics only
    {'Name': 'shoot', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},

    # Symbols
    {'Name': 'solid arrow', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'hollow arrow', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
    {'Name': 'gen arrow', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},

    # xUML state machine diagram
    {'Name': 'transition', 'Form': 'shape', 'Drawing type': 'xUML state machine diagram'},
    {'Name': 'event', 'Form': 'text', 'Drawing type': 'xUML state machine diagram'},
    {'Name': 'activity', 'Form': 'text', 'Drawing type': 'xUML state machine diagram'},
    {'Name': 'state name', 'Form': 'text', 'Drawing type': 'xUML state machine diagram'},
    {'Name': 'state compartment', 'Form': 'shape', 'Drawing type': 'xUML state machine diagram'},
    # Symbols
    {'Name': 'hollow large circle', 'Form': 'shape', 'Drawing type': 'xUML state machine diagram'},
    {'Name': 'solid dot', 'Form': 'shape', 'Drawing type': 'xUML state machine diagram'},

    # Domain diagram
    {'Name': 'domain node', 'Form': 'shape', 'Drawing type': 'Starr domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'Drawing type': 'Starr domain diagram'},

    {'Name': 'domain node', 'Form': 'shape', 'Drawing type': 'xUML domain diagram'},
    {'Name': 'bridge', 'Form': 'shape', 'Drawing type': 'xUML domain diagram'},

    # Collaboration diagram
    {'Name': 'overview class', 'Form': 'shape', 'Drawing type': 'Starr collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'Drawing type': 'Starr collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'Drawing type': 'Starr collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'Drawing type': 'Starr collaboration diagram'},

    {'Name': 'overview class', 'Form': 'shape', 'Drawing type': 'xUML collaboration diagram'},
    {'Name': 'collaboration', 'Form': 'shape', 'Drawing type': 'xUML collaboration diagram'},
    {'Name': 'message', 'Form': 'text', 'Drawing type': 'xUML collaboration diagram'},
    {'Name': 'sync arrow', 'Form': 'shape', 'Drawing type': 'xUML collaboration diagram'}
]