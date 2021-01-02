"""
shape_presentation_instances.py
"""

population = [
    # Starr class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'hide'},
    {'Asset': 'solid arrow', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'default', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},

    # xuml class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawing type': 'xuml class diagram', 'Line style': 'margin'},

    # Shlaer-Mellor class default
    {'Asset': 'class compartment', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'default', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # Starr class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram',
     'Line style': 'normal'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'margin'},
    {'Asset': 'solid arrow', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'hollow arrow', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    {'Asset': 'gen arrow', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram', 'Line style': 'normal'},
    # Only for diagnostics
    {'Asset': 'shoot', 'Presentation': 'diagnostic', 'drawing type': 'Starr class diagram',
     'Line style': 'connector highlight'},

    # xuml class diagnostic
    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram', 'Line style': 'dashed'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawing type': 'xuml class diagram', 'Line style': 'margin'},

    {'Asset': 'class compartment', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'binary association connector', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'generalization connector', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram',
     'Line style': 'connector highlight'},
    {'Asset': 'imported class compartment', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'dashed'},
    {'Asset': 'associative mult stem', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'normal'},
    {'Asset': 'grid', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'grid'},
    {'Asset': 'margin', 'Presentation': 'diagnostic', 'drawing type': 'Shlaer-Mellor class diagram', 'Line style': 'margin'},

    # xuml state default
    {'Asset': 'transition', 'Presentation': 'default', 'drawing type': 'xuml state machine diagram', 'Line style': 'normal'},
    {'Asset': 'state compartment', 'Presentation': 'default', 'drawing type': 'xuml state machine diagram', 'Line style': 'normal'},
    {'Asset': 'solid dot', 'Presentation': 'default', 'drawing type': 'xuml state machine diagram',
     'Line style': 'normal'},
    {'Asset': 'hollow large circle', 'Presentation': 'default', 'drawing type': 'xuml state machine diagram',
     'Line style': 'normal'},

]
