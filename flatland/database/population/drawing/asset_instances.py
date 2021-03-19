"""
asset_instances.py
"""

population = [
    # Grid
    {'Name': 'column boundary', 'Form': 'shape', 'Drawing type': 'Grid Diagnostic'},
    {'Name': 'row boundary', 'Form': 'shape', 'Drawing type': 'Grid Diagnostic'},
    {'Name': 'grid boundary', 'Form': 'shape', 'Drawing type': 'Grid Diagnostic'},
    {'Name': 'grid label', 'Form': 'text',  'Drawing type': 'Grid Diagnostic'},

    # Frame OS Engineer large
    # Open field assets
    {'Name': 'Open title', 'Form': 'text', 'Drawing type': 'OS Engineer large frame'},
    {'Name': 'Open copyright notice', 'Form': 'text', 'Drawing type': 'OS Engineer large frame'},
    # Title block assets
    {'Name': 'Block title', 'Form': 'text', 'Drawing type': 'OS Engineer large frame'},
    {'Name': 'Block body', 'Form': 'text', 'Drawing type': 'OS Engineer large frame'},
    {'Name': 'Block border', 'Form': 'shape', 'Drawing type': 'OS Engineer large frame'},

    # Frame OS Engineer medium
    # Open field assets
    {'Name': 'Open title', 'Form': 'text', 'Drawing type': 'OS Engineer medium frame'},
    {'Name': 'Open copyright notice', 'Form': 'text', 'Drawing type': 'OS Engineer medium frame'},
    # Title block assets
    {'Name': 'Block title', 'Form': 'text', 'Drawing type': 'OS Engineer medium frame'},
    {'Name': 'Block body', 'Form': 'text', 'Drawing type': 'OS Engineer medium frame'},
    {'Name': 'Block border', 'Form': 'shape', 'Drawing type': 'OS Engineer medium frame'},

    # Frame OS Engineer large
    # Open field assets
    {'Name': 'Open title', 'Form': 'text', 'Drawing type': 'TRI MBSE large frame'},
    {'Name': 'Open copyright notice', 'Form': 'text', 'Drawing type': 'TRI MBSE large frame'},
    # Title block assets
    {'Name': 'Block title', 'Form': 'text', 'Drawing type': 'TRI MBSE large frame'},
    {'Name': 'Block body', 'Form': 'text', 'Drawing type': 'TRI MBSE large frame'},
    {'Name': 'Block border', 'Form': 'shape', 'Drawing type': 'TRI MBSE large frame'},
    #
    # # Frame OS Engineer small
    # # Open field assets
    # {'Name': 'Open title small', 'Form': 'text', 'Drawing type': 'OS Engineer small'},
    # {'Name': 'Open copyright notice small', 'Form': 'text', 'Drawing type': 'OS Engineer small'},
    # # Title block assets
    # {'Name': 'Block title small', 'Form': 'text', 'Drawing type': 'OS Engineer small'},
    # {'Name': 'Block body small', 'Form': 'text', 'Drawing type': 'OS Engineer small'},
    # {'Name': 'Block border small', 'Form': 'shape', 'Drawing type': 'OS Engineer small'},

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
    {'Name': 'name underlay', 'Form': 'shape', 'Drawing type': 'Starr class diagram'},
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