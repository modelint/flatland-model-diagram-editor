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
]