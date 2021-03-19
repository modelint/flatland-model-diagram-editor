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

    # Starr class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'solid arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'name underlay', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Line style': 'hidden'},

    # xUML class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Line style': 'margin'},

    # Shlaer-Mellor class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # Starr class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'margin'},
    {'Asset': 'solid arrow', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram', 'Line style': 'normal'},
    # Only for diagnostics
    {'Asset': 'shoot', 'Presentation': 'diagnostic', 'Drawing type': 'Starr class diagram',
     'Line style': 'connector highlight'},

    # xUML class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'Drawing type': 'xUML class diagram', 'Line style': 'margin'},

    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'Drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # xUML state default
    {'Asset': 'transition', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state compartment', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Line style': 'normal'},
    {'Asset': 'solid dot', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram',
     'Line style': 'normal'},
    {'Asset': 'hollow large circle', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram',
     'Line style': 'normal'},

]
