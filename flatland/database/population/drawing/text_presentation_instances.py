"""
text_presentation_instances.py
"""

population = [
    # Grid Diagnostic
    {'Asset': 'grid label', 'Presentation': 'default', 'Drawing type': 'Grid Diagnostic',
     'Text style': 'coordinate', 'Underlay': False},

    # Frame OS Engineer, default
    # Large
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Corner Title Large', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'boilerplate', 'Underlay': False},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Block Title Large', 'Underlay': False},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'OS Engineer large frame',
     'Text style': 'Block Body Large', 'Underlay': False},

    # Medium
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Corner Title Medium', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'boilerplate', 'Underlay': False},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Block Title Medium', 'Underlay': False},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'OS Engineer medium frame',
     'Text style': 'Block Body Medium', 'Underlay': False},

    # Small
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'Block Title Small', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'boilerplate', 'Underlay': False},
    {'Asset': 'Open author', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open modification date', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open document id', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open version', 'Presentation': 'default', 'Drawing type': 'OS Engineer small frame',
     'Text style': 'Block Body Small', 'Underlay': False},

    # Frame TRI MBSE, default
    # Large
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Corner Title Large', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Footer Central', 'Underlay': False},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Block Title Large', 'Underlay': False},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'TRI MBSE large frame',
     'Text style': 'Block Body Large', 'Underlay': False},

    # Medium
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Corner Title Medium', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'boilerplate', 'Underlay': False},
    {'Asset': 'Block title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Block Title Medium', 'Underlay': False},
    {'Asset': 'Block body', 'Presentation': 'default', 'Drawing type': 'TRI MBSE medium frame',
     'Text style': 'Block Body Medium', 'Underlay': False},

    # Small
    {'Asset': 'Open title', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'Block Title Small', 'Underlay': False},
    {'Asset': 'Open copyright notice', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'boilerplate', 'Underlay': False},
    {'Asset': 'Open author', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open modification date', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open document id', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'Block Body Small', 'Underlay': False},
    {'Asset': 'Open version', 'Presentation': 'default', 'Drawing type': 'TRI MBSE small frame',
     'Text style': 'Block Body Small', 'Underlay': False},

    # Starr class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': True},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9italic', 'Underlay': False},
    {'Asset': 'imported class name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p12title', 'Underlay': False},
    {'Asset': 'imported class attribute', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p12title', 'Underlay': False},
    {'Asset': 'class attribute', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'class method', 'Presentation': 'default', 'Drawing type': 'Starr class diagram', 'Text style': 'p9body', 'Underlay': False},

    # xUML class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9italic', 'Underlay': False},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p12title', 'Underlay': False},
    {'Asset': 'attributes', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'methods', 'Presentation': 'default', 'Drawing type': 'xUML class diagram', 'Text style': 'p9body', 'Underlay': False},

    # Shlaer-Mellor class diagram, default
    {'Asset': 'label', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'binary association name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'generalization name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'class mult name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'see also', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9italic', 'Underlay': False},
    {'Asset': 'class name', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p12title', 'Underlay': False},
    {'Asset': 'attributes', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'methods', 'Presentation': 'default', 'Drawing type': 'Shlaer-Mellor class diagram', 'Text style': 'p9body', 'Underlay': False},

    # xUML state machine diagram, default
    {'Asset': 'transition name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'initial transition name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'state activity', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p9body', 'Underlay': False},
    {'Asset': 'state name', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram', 'Text style': 'p12title', 'Underlay': False},
    {'Asset': 'state name only', 'Presentation': 'default', 'Drawing type': 'xUML state machine diagram',
     'Text style': 'p12title', 'Underlay': False},
]