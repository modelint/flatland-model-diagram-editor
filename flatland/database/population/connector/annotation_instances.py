"""
annotation_instances.py
"""
population = [
    # Class diagram

    # xUML notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': 'Mc mult', 'Label': '0..*',
     'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': 'M mult', 'Label': '1..*',
     'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': '1c mult', 'Label': '0..1',
     'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': '1 mult', 'Label': '1',
     'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},

    # Associative multiplicity (no notation for 1 multiplicity associative)
    {'Stem type': 'associative mult', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': 'M mult', 'Label': '{M}',
     'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},

    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'xUML', 'Semantic': 'superclass',
     'Label': '{disjoint, complete}', 'Default stem side': '+', 'Vertical stem offset': 15,
     'Horizontal stem offset': 15},

    # Shlaer-Mellor notation
    # Binary multiplicity
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor', 'Semantic': 'Mc mult',
     'Label': 'c', 'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},
    {'Stem type': 'class mult', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor', 'Semantic': '1c mult',
     'Label': 'c', 'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9},

    # Generalization
    {'Stem type': 'superclass', 'Diagram type': 'class', 'Notation': 'Shlaer-Mellor', 'Semantic': 'superclass',
     'Label': 'is a', 'Default stem side': '+', 'Vertical stem offset': 9, 'Horizontal stem offset': 9}
]
