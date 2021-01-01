"""
dash_pattern_instances.py
"""

population = [
    # To simplify the database, a non-dashed line has the meaningless 0,0 value.
    # Otherwise, we would have to subclass line styles into dashed and non-dashed
    {'Name': 'no dash', 'Solid': 0, 'Blank': 0},

    # only one real dash pattern for now, used for UML assoc classes and imported classes
    {'Name': 'even dash', 'Solid': 9, 'Blank': 9}
]