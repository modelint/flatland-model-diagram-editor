"""
stem_end_decoration_instances.py
"""
population = [
    # Class diagram

    # Starr notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'Mc mult', 'Symbol': 'double hollow arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1c mult', 'Symbol': 'hollow arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1 mult', 'Symbol': 'solid arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'M mult', 'Symbol': 'double solid arrow', 'End': 'root'},
    # Associative multiplicity
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1 mult', 'Symbol': 'solid arrow', 'End': 'vine'},
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'M mult', 'Symbol': 'double solid arrow', 'End': 'vine'},
    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'superclass', 'Symbol': 'gen arrow', 'End': 'root'},

    # xUML notation
    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': 'superclass', 'Symbol': 'gen arrow', 'End': 'root'},

    # Shlaer-Mellor notation
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'Mc mult', 'Symbol': 'double open arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1c mult', 'Symbol': 'open arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1 mult', 'Symbol': 'open arrow', 'End': 'root'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'M mult', 'Symbol': 'double open arrow', 'End': 'root'},
    # Associative multiplicity
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1 mult', 'Symbol': 'open arrow', 'End': 'vine'},
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'M mult', 'Symbol': 'double open arrow', 'End': 'vine'},
    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'superclass', 'Symbol': 'superclass cross', 'End': 'vine'},

    # State machine diagram
    {'Stem type': 'to state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'target state', 'Symbol': 'solid arrow', 'End': 'root'},

    # Both ends of unary stem are decoreated for xUML initial transition
    {'Stem type': 'to initial state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'initial pseudo state', 'Symbol': 'solid arrow', 'End': 'root'},
    {'Stem type': 'to initial state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'initial pseudo state', 'Symbol': 'solid small dot', 'End': 'vine'},

    {'Stem type': 'from deletion state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'final pseudo state', 'Symbol': 'circled dot', 'End': 'vine'},

    # Domain diagram
    # Starr
    {'Stem type': 'to service', 'Diagram type': 'domain', 'Notation': 'Starr',
     'Semantic': 'require', 'Symbol': 'solid arrow', 'End': 'root'},
    # xUML
    {'Stem type': 'to service', 'Diagram type': 'domain', 'Notation': 'xUML',
     'Semantic': 'require', 'Symbol': 'open arrow', 'End': 'root'}
]