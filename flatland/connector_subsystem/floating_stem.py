"""
floating_stem.py
"""

from flatland.connector_subsystem.stem import Stem, StemName
from flatland.connector_subsystem.stem_type import StemType
from flatland.datatypes.connection_types import NodeFace
from flatland.datatypes.geometry_types import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.connector_subsystem.connector import Connector
    from flatland.node_subsystem.node import Node


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
