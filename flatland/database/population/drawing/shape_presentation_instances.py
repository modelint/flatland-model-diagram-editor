"""
shape_presentation_instances.py
"""

population = [
    # Grid Diagnostic
    {'Asset': 'row boundary', 'Presentation': 'default', 'Drawing type': 'Grid Diagnostic',
     'Line style': 'grid'},
    {'Asset': 'column boundary', 'Presentation': 'default', 'Drawing type': 'Grid Diagnostic',
     'Line style': 'grid'},
    {'Asset': 'grid boundary', 'Presentation': 'default', 'Drawing type': 'Grid Diagnostic',
     'Line style': 'margin'},

    # Frame: OS Engineer default
    {'Asset': 'Block border', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Line style': 'double'},
    {'Asset': 'Block border', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Line style': 'normal'},
    # Frame: TRI MBSE default
    {'Asset': 'Block border', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Line style': 'double'},
    {'Asset': 'Block border', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Line style': 'normal'},

    # Starr class default
    {'Asset': 'class name compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'class attribute compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'class method compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class name compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'imported class attribute compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'solid arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},

    # xUML class default
    {'Asset': 'class name compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'class attribute compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'class method compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'margin'},

    # Shlaer-Mellor class default
    {'Asset': 'class name compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'class attribute compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'class method compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # xUML state default
    {'Asset': 'initial transition connector', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'deletion transition connector', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'transition connector', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state name compartment', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state name only compartment', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state activity compartment', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'solid arrow', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'solid small dot', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram',
     'Line style': 'normal'},
    {'Asset': 'hollow large circle', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram',
     'Line style': 'normal'},

]
