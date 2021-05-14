"""
text_presentation_instances.py
"""

population = [
    # Grid Diagnostic
    {'Asset': 'grid label', 'Presentation': 'default', 'Drawing type': 'Grid Diagnostic',
     'Text style': 'coordinate'},

    # Frame OS Engineer, default
    # Large
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Corner Title Large'},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'boilerplate'},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Block Title Large'},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Block Body Large'},

    # Medium
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Corner Title Medium'},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'boilerplate'},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Block Title Medium'},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Block Body Medium'},

    # Frame TRI MBSE, default
    # Large
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Corner Title Large'},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Footer Central'},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Block Title Large'},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Block Body Large'},

    # Medium
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Corner Title Medium'},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'boilerplate'},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Block Title Medium'},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Block Body Medium'},

    #
    # Small
    # {'Asset': 'Open title large', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
    #  'Text style': 'Corner Title Small'},
    # {'Asset': 'Open copyright notice large', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
    #  'Text style': 'boilerplate'},
    # {'Asset': 'Block title large', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
    #  'Text style': 'Block Title Small'},
    # {'Asset': 'Block body large', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
    #  'Text style': 'Block Body Small'},

    # Starr class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9italic'},
    {'Asset': 'imported class name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p12title'},
    {'Asset': 'imported class attribute', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p12title'},
    {'Asset': 'class attribute', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},
    {'Asset': 'class method', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body'},

    # xUML class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9italic'},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p12title'},
    {'Asset': 'attributes', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},
    {'Asset': 'methods', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body'},

    # Shlaer-Mellor class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9italic'},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p12title'},
    {'Asset': 'attributes', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},
    {'Asset': 'methods', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body'},

    # xUML state machine diagram, default
    {'Asset': 'transition name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body'},
    {'Asset': 'initial transition name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body'},
    {'Asset': 'state activity', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body'},
    {'Asset': 'state name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p12title'}
]