"""
anchored_tree_stem.py
"""

from flatland.connector_subsystem.anchored_stem import AnchoredStem
from flatland.datatypes.connection_types import AnchorPosition, NodeFace
from flatland.connector_subsystem.stem_type import StemType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.connector_subsystem.connector import Connector
    from flatland.node_subsystem.node import Node


class AnchoredTreeStem(AnchoredStem):
    """
    Any Stem within a Tree Connector attached to a user specified anchor position is an Anchored Tree Stem.
    """
    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, anchor_position: AnchorPosition):
        AnchoredStem.__init__(self, connector, stem_type, semantic, node, face, anchor_position, name=None)

        # Nothing special going on here yet

