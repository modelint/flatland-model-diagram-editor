"""
anchored_leaf_stem.py
"""

from flatland.connector_subsystem.anchored_tree_stem import AnchoredTreeStem
from flatland.datatypes.connection_types import NodeFace, AnchorPosition
from flatland.connector_subsystem.stem_type import StemType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.connector_subsystem.connector import Connector
    from flatland.node_subsystem.node import Node


class AnchoredLeafStem(AnchoredTreeStem):
    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, anchor_position: AnchorPosition):
        AnchoredTreeStem.__init__(
            self, connector, stem_type, semantic, node, face, anchor_position)
