"""
decorated_stem_instances.py
"""

population = [
    # Class diagram

    # Starr notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'Mc mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1c mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1 mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'M mult', 'Stroke': 'normal'},

    # Associative multiplicity
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': '1 mult', 'Stroke': 'normal'},
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'M mult', 'Stroke': 'normal'},

    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'Starr',
     'Semantic': 'superclass', 'Stroke': 'normal'},

    # xUML notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': 'Mc mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': '1c mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': '1 mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': 'M mult', 'Stroke': 'normal'},

    # Associative multiplicity (no notation for 1 multiplicity associative)
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': '1 mult', 'Stroke': 'dashed'},
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': 'M mult', 'Stroke': 'dashed'},

    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'xUML',
     'Semantic': 'superclass', 'Stroke': 'normal'},

    # Shlaer-Mellor notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'Mc mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1c mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1 mult', 'Stroke': 'normal'},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'M mult', 'Stroke': 'normal'},

    # Associative multiplicity
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': '1 mult', 'Stroke': 'normal'},
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'M mult', 'Stroke': 'normal'},

    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor',
     'Semantic': 'superclass', 'Stroke': 'normal'},

    # State machine diagram
    {'Stem type': 'to state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'target state', 'Stroke': 'normal'},

    # Both ends of unary stem are decoreated for xUML initial transition
    {'Stem type': 'to initial state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'initial pseudo state', 'Stroke': 'normal'},
    {'Stem type': 'from deletion state', 'Diagram type': 'state machine', 'Notation': 'xUML',
     'Semantic': 'final pseudo state', 'Stroke': 'normal'},

    # Domain diagram
    # Starr
    {'Stem type': 'to service', 'Diagram type': 'domain', 'Notation': 'Starr',
     'Semantic': 'require', 'Stroke': 'normal'},
    # xUML
    {'Stem type': 'to service', 'Diagram type': 'domain', 'Notation': 'xUML',
     'Semantic': 'require', 'Stroke': 'normal'}
]