""" floating_binary_stem.py """

from flatland.connector_subsystem.stem import Stem
from flatland.datatypes.connection_types import NodeFace, StemName
from flatland.datatypes.geometry_types import Position
from flatland.connector_subsystem.stem_type import StemType
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flatland.connector_subsystem.connector import Connector
    from flatland.connector_subsystem.anchored_stem import AnchoredStem


class FloatingBinaryStem(Stem):
    """
    A Stem on a Straight Binary Connector that is positioned laterally on a Node face
    so that it lines up with an opposing Anchored Stem. Consequenlty, no anchor position
    is specified, just an x or y location representing where the straight connector line intersects
    the floating stem's attached node face.

    """

    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str,
                 node: 'Node', face: NodeFace, projecting_stem: 'AnchoredStem', name: Optional[StemName]):
        """
        Constructor

        We will use either the x or y of our opposing Anchored Stem and then set the other coordinate
        to coincide with the Node face position attached to Floating Stem since this is a Straight Binary
        Connector

        :param connector:
        :param stem_type:
        :param semantic:
        :param node:
        :param face:
        :param projecting_stem:
        """

        # Initially set the Floating Stem root end to match the Projecting Stem root end
        x, y = projecting_stem.Root_end

        # left and right faces are vertical, so they determine the x coordinate
        if face == NodeFace.LEFT:
            x = node.Canvas_position.x
        elif face == NodeFace.RIGHT:
            x = node.Canvas_position.x + node.Size.width
        # top and bottom faces are horizontal, so they determine the y coordinate
        elif face == NodeFace.TOP:
            y = node.Canvas_position.y + node.Size.height
        elif face == NodeFace.BOTTOM:
            y = node.Canvas_position.y

        # Stem initialized with our computed root end
        root = Position(x, y)
        Stem.__init__(self, connector, stem_type, semantic, node, face, root_position=root, name=name)
