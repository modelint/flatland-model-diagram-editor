"""
tertiary_stem.py
"""

from flatland.connector_subsystem.anchored_stem import AnchoredStem
from flatland.connector_subsystem.stem_type import StemType
from flatland.datatypes.connection_types import HorizontalFace, NodeFace, AnchorPosition, StemName
from flatland.datatypes.geometry_types import Position
from flatland.geometry_domain.linear_geometry import nearest_parallel_segment
from typing import TYPE_CHECKING, Set, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.node import Node
    from flatland.connector_subsystem.binary_connector import BinaryConnector


class TertiaryStem(AnchoredStem):
    """
    An Anchored Stem that reaches from a Node face at its root end and attaches its vine end to the
    line segment drawn for a Binary Connector.
    """

    def __init__(self, connector: 'BinaryConnector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, anchor_position: AnchorPosition, parallel_segs: Set[tuple],
                 name: Optional[StemName] = None):
        """
        Constructor

        :param connector:  Part of this Binary Connector
        :param stem_type: Specifies universal characteristics of this Stem
        :param semantic: Meaning of this Stem
        :param node: Is rooted on this Node
        :param face: Is rooted from this Node face
        :param anchor_position: Position of the Root as specified by the user
        :param parallel_segs: All binary connector line segments parallel to the rooted Node face
        :param name: Optional name to be drawn next to stem vine end
        """
        AnchoredStem.__init__(self, connector, stem_type, semantic, node, face, anchor_position, name)
        # At this point the anchor_position has been resolved to an x,y coordinate on the node face

        self.Root_start = None
        self.Vine_start = None

        # Compute the vine end so that it touches the closest Binary Connector bend line segment
        # away from the root node face
        asc = True if face in {NodeFace.TOP, NodeFace.RIGHT} else False
        axis = nearest_parallel_segment(psegs=parallel_segs, point=self.Root_end, ascending=asc)
        self.Vine_end = Position(self.Root_end.x, axis) if face in HorizontalFace else Position(axis, self.Root_end.y)

    def render(self):
        """
        Create line from root end to the vine end attached to the Binary Connector line
        """
        layer = self.Connector.Diagram.Layer
        layer.add_line_segment(asset=self.Stem_type.Name+' stem', from_here=self.Root_end, to_there=self.Vine_end)
        super().render()