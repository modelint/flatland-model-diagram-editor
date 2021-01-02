"""
geometry_types.py

Data types for 2D geometry and alignment
"""

from typing import NewType
from collections import namedtuple
from enum import Enum

Coordinate = NewType('Coordinate', float )
Distance = int


class VertAlign(Enum):
    """The numeric values are low to high in the axis direction"""
    BOTTOM = 0
    CENTER = 1
    TOP = 2


class HorizAlign(Enum):
    """The numeric values are low to high in the axis direction"""
    LEFT = 0
    CENTER = 1
    RIGHT = 2


Rectangle = namedtuple('Rectangle', 'line_style lower_left, size')
Position = namedtuple('Position', 'x y')
Line_Segment = namedtuple('Line_Segment', 'from_position to_position')
Rect_Size = namedtuple('Rect_Size', 'height width')
Alignment = namedtuple('Alignment', 'vertical horizontal')
Padding = namedtuple('Padding', 'top bottom left right')
