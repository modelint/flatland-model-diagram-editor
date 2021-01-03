"""
general_types.py - Model level types that are used across multiple domains
"""

from typing import NewType

Text = str
PosInt = NewType('PosInt', int)

LaneNum = NewType('LaneNum', PosInt)  # Row or column number (a positive integer)
Index = NewType('Index', PosInt)  # A numeric array index (a positive integer)


def ok_posint(i: int) -> bool:
    return i >= 0
