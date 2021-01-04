"""
floating_stem.py
"""

from stem import Stem, StemName
from stem_type import StemType
from connection_types import NodeFace
from geometry_types import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from connector import Connector
    from node import Node


class FloatingStem(Stem):
    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, root_position: Position, name: StemName = None):
        """
        Constructor

        :param connector:
        :param stem_type:
        :param semantic:
        :param node:
        :param face:
        :param root_position:
        """
        Stem.__init__(self, connector, stem_type, semantic, node, face, root_position, name)
