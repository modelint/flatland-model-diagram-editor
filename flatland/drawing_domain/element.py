"""
element.py - Fundamental drawing elements such as shapes and text lines
"""
from collections import namedtuple

Circle = namedtuple('_Circle', 'center radius border_style fill')
"""Circle"""
Polygon = namedtuple('_Polygon', 'vertices border_style fill')
"""Closed polygon (other than a rectangle) that can be filled"""
Line_Segment = namedtuple('_Line_Segment', 'from_here to_there style')
"""A line segment is drawn from one point on the Tablet to another using some line drawing style"""
Rectangle = namedtuple('_Rectangle', 'upper_left size border_style fill radius top bottom')
"""A rectangle is positioned at its lower left corner and then drawn with the specified size"""
FillRect = namedtuple('_FillRect', 'upper_left size color')
"""A borderless rectangle is filled with the specified color"""
Text_line = namedtuple('_Text_line', 'lower_left text style')
"""A line of text (no CR/LF characters) rendered with a given style"""
Image = namedtuple('_Image', 'resource_path upper_left size')
"""A png or jpeg image file and a position"""
