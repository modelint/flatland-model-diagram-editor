"""
connection_types.py

Data types to support Connectors and Stems
"""

from enum import Enum
from collections import namedtuple
from typing import NewType

AnchorPosition = NewType('AnchorPosition', int)

NameSpec = namedtuple('NameSpec', 'axis_buffer end_buffer default_name optional')
"""
Specifies how a connector or stem name is to be placed and filled

    Attributes

    - axis_buffer -- (Buffer) Space between connector line and name bounding box
    - end_buffer -- (Buffer) Space between connector line and name bounding box
    - default_name -- (Text) This name is filled in if the user does not supply a name and the name is not optional
    - optional -- (Boolean) No name is rendered if the user does not provide one
"""

Buffer = namedtuple('Buffer', 'vertical horizontal')
"""
A white space buffer between a graphical element and some other graphical element

    Attributes

    - horizontal -- (Distance) space above or below an element
    - vertical -- (Distance) space right or left of an element
"""
StemName = namedtuple('StemName', 'text side axis_offset end_offset')
"""
User specification of name text placed near a Stem

    Attributes

    - text -- A TextBlock instance
    - side -- ( 1 | -1 ) Which side of the Stem (top bottom) or (right left)
    - axis_offset -- A positive or negative non-zero integer specifying axis side and distance from the axis
    - end_offset -- A positive integer specifying non-default offset distance from the end of the stem
"""
ConnectorName = namedtuple('ConnectorName', 'text side bend')
"""
User specification of name text placed near the center of a Connector

    Attributes

    - text -- The text to be written
    - side -- ( 1 | -1 ) Which side of the Connector (top bottom) or (right left)
    - bend -- The clockwise bend number starting from 1, default is 1, positive non-zero integer
"""

Path = namedtuple('Path', 'lane rut')
"""
A position within a row or column where a Connector line segment is drawn

    Attributes
    
    - lane -- A row or column
    - rut -- A numbered position within the lane
"""
DecoratedStemEnd = namedtuple('DecoratedStemEnd', 'stem_type semantic diagram_type notation end')


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


class StemEnd(Enum):
    ROOT = 0
    VINE = 1


class NodeFace(Enum):
    """
    Values are multiplied by absolute distance to get an x or y coordinate.
    """
    TOP = 0
    BOTTOM = 1
    RIGHT = 2
    LEFT = 3


HorizontalFace = {NodeFace.TOP, NodeFace.BOTTOM}

OppositeFace = {
    NodeFace.TOP: NodeFace.BOTTOM,
    NodeFace.BOTTOM: NodeFace.TOP,
    NodeFace.LEFT: NodeFace.RIGHT,
    NodeFace.RIGHT: NodeFace.LEFT
}


class Geometry(Enum):
    """
    This describes the way that a Connector is drawn, pulling together all of its Stems. Many geometries are possible,
    but only a handful are supported which should cover a wide range of diagramming possibilities.

    Unary (U) – Relationship is rooted in some Node on one end and not connected on the other end. An initial
    transition on a state machine diagram is one example where the target state is connected and the other end
    of the transition just has a dark circle drawn at the other end (not a Node). It consists of a single Stem.

    Binary (B) – Relationship is drawn from one Node face position to another on the same or a different Node.
    This could be a state transition with a from and to state or a binary association from one class to another
    or a reflexive relationship starting and ending on the same class or state. It consists of two Stems, one
    attached to each Node face position connected together with a line.

    Ternary (T) – This is a binary relationship with an additional Stem connecting to the line between the binary
    relationship Stems. A typical example is a class diagram association class where a third Stem emanates from the
    association class Node connecting to the line between the binary relationship Stems.

    Hierarchical (H) – Here one Node is a root connecting to two or more other Nodes. A Stem emanates from the root
    Node and another type of Stem emanates from each of the subsidiary Nodes and one or more lines are drawn to
    connect all the Stems. A class diagram generalization relationship is a typical case.
    """
    U = "unary"
    B = "binary"
    T = "ternary"
    H = "hierarchical"
