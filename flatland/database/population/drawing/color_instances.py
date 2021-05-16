"""
color_instances.py
"""
from collections import namedtuple
population = [
    {"Name": 'white', 'R': 255, 'G': 255, 'B': 255},
    {"Name": 'black', 'R': 0, 'G': 0, 'B': 0},
    {"Name": 'grid blue', 'R': 51, 'G': 235, 'B': 186},   # To paint the canvas node grid for diagnostics
    {"Name": 'purple', 'R': 125, 'G': 51, 'B': 235},      # Diagnostics for highlighting connectors
    {"Name": 'horrible red', 'R': 255, 'G': 0, 'B': 0},   # Used to highlight errors
    {"Name": 'gold', 'R': 255, 'G':219, 'B': 44},         # Used for margin diagnostic
    {"Name": 'toyota red', 'R': 236, 'G': 10, 'B': 30},   # Bright red in TRI logo
    {"Name": 'block blue', 'R': 0, 'G': 64, 'B': 128},    # Blue in modelint block titles

    # Canvas colors
    {"Name": 'gray', 'R': 121, 'G': 121, 'B': 121},
    {"Name": 'yellow', 'R': 255, 'G': 252, 'B': 121},
    {"Name": 'aqua', 'R': 0, 'G': 150, 'B': 255},
    {"Name": 'teal', 'R': 87, 'G': 181, 'B': 174},
    {"Name": 'pink', 'R': 246, 'G': 196, 'B': 249},
    {"Name": 'butterscotch', 'R': 206, 'G': 124, 'B': 65},
    {"Name": 'light purple', 'R': 146, 'G': 102, 'B': 173},
    {"Name": 'brown', 'R': 143, 'G': 108, 'B': 72},
    {"Name": 'orange', 'R': 197, 'G': 150, 'B': 35},
]