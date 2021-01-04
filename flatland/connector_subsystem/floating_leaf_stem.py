"""
floating_leaf_stem.py
"""
from flatland.connector_subsystem.stem import StemName
from flatland.connector_subsystem.floating_stem import FloatingStem
from flatland.connector_subsystem.stem_type import StemType
from flatland.datatypes.connection_types import NodeFace
from flatland.datatypes.geometry_types import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.connector_subsystem.connector import Connector
    from flatland.node_subsystem.node import Node
    from flatland.connector_subsystem.grafted_branch import GraftedBranch


class FloatingLeafStem(FloatingStem):
    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, grafted_branch: 'GraftedBranch', root_position: Position,
                 name: StemName = None):
        FloatingStem.__init__(self, connector, stem_type, semantic, node, face, root_position, name)
        self.Grafted_branch = grafted_branch
