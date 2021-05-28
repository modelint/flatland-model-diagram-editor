"""
color_instances.py
"""
from collections import namedtuple
population = [
    # Canvas colors
    # Blues
    {"Name": 'sky', 'R': 199, 'G': 227, 'B': 245, 'Purpose': 'canvas'},
    {"Name": 'blue steel', 'R': 159, 'G': 172, 'B': 186, 'Purpose': 'canvas'},
    {"Name": 'teal', 'R': 125, 'G': 181, 'B': 175, 'Purpose': 'canvas'},

    # Grays
    {"Name": 'nickel', 'R': 146, 'G': 146, 'B': 146, 'Purpose': 'canvas'},
    {"Name": 'silver', 'R': 214, 'G': 214, 'B': 214, 'Purpose': 'canvas'},
    {"Name": 'magnesium', 'R': 192, 'G': 192, 'B': 192, 'Purpose': 'canvas'},
    {"Name": 'aluminum', 'R': 169, 'G': 169, 'B': 169, 'Purpose': 'canvas'},

    # Greens
    {"Name": 'clover', 'R': 205, 'G': 231, 'B': 178, 'Purpose': 'canvas'},
    {"Name": 'institutional', 'R': 192, 'G': 204, 'B': 160, 'Purpose': 'canvas'},
    {"Name": 'olive', 'R': 154, 'G': 152, 'B': 36, 'Purpose': 'canvas'},

    # Yellows
    {"Name": 'butter', 'R': 255, 'G': 255, 'B': 191, 'Purpose': 'canvas'},
    {"Name": 'limoncello', 'R': 255, 'G': 255, 'B': 128, 'Purpose': 'canvas'},
    {"Name": 'cantaloupe', 'R': 255, 'G': 212, 'B': 121, 'Purpose': 'canvas'},
    {"Name": 'peach', 'R': 255, 'G': 197, 'B': 95, 'Purpose': 'canvas'},

    # Oranges
    {"Name": 'pumpkin', 'R': 206, 'G': 124, 'B': 65, 'Purpose': 'canvas'},
    {"Name": 'autumn', 'R': 197, 'G': 150, 'B': 35, 'Purpose': 'canvas'},

    # Reds
    {"Name": 'bubble gum', 'R': 243, 'G': 212, 'B': 222, 'Purpose': 'canvas'},
    {"Name": 'pink eraser', 'R': 240, 'G': 176, 'B': 158, 'Purpose': 'canvas'},

    # Purples
    {"Name": 'tutti frutti', 'R': 246, 'G': 196, 'B': 249, 'Purpose': 'canvas'},
    {"Name": 'light purple', 'R': 237, 'G': 187, 'B': 251, 'Purpose': 'canvas'},
    {"Name": 'harolds purple crayon', 'R': 164, 'G': 161, 'B': 211, 'Purpose': 'canvas'},

    # Browns
    {"Name": 'dead leaf', 'R': 180, 'G': 142, 'B': 85, 'Purpose': 'canvas'},

    # DIAGNOSTIC COLORS (not suitable for backgrounds)
    {"Name": 'white', 'R': 255, 'G': 255, 'B': 255, 'Purpose': 'diagnostic'},
    {"Name": 'black', 'R': 0, 'G': 0, 'B': 0, 'Purpose': 'diagnostic'},
    {"Name": 'grid blue', 'R': 51, 'G': 235, 'B': 186, 'Purpose': 'diagnostic'},  # To paint the canvas node grid for diagnostics
    {"Name": 'purple', 'R': 125, 'G': 51, 'B': 235, 'Purpose': 'diagnostic'},  # Diagnostics for highlighting connectors
    {"Name": 'horrible red', 'R': 255, 'G': 0, 'B': 0, 'Purpose': 'diagnostic'},  # Used to highlight errors
    {"Name": 'gold', 'R': 255, 'G': 219, 'B': 44, 'Purpose': 'diagnostic'},  # Used for margin diagnostic

    # Logo colors
    {"Name": 'toyota red', 'R': 236, 'G': 10, 'B': 30, 'Purpose': 'logo'},  # Bright red in TRI logo
    {"Name": 'block blue', 'R': 0, 'G': 64, 'B': 128, 'Purpose': 'logo'},  # Blue in modelint block titles

]