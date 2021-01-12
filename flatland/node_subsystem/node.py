"""
node.py
"""
import logging
from flatland.flatland_exceptions import UnsupportedNodeType
from flatland.datatypes.geometry_types import Rect_Size, Position, Alignment
from flatland.node_subsystem.compartment import Compartment
from flatland.datatypes.connection_types import NodeFace
from typing import TYPE_CHECKING, List, Optional
from flatland.node_subsystem.diagram_layout_specification import DiagramLayoutSpecification as diagram_layout

if TYPE_CHECKING:
    from flatland.node_subsystem.grid import Grid


class Node:
    """
    This is a rectangular diagram symbol consisting of one or more UML style Compartments
    stacked in a vertical order.

        Attributes

        - Content -- The unformatted text that will be drawn into the Node's Compartments organized as a dictionary
          with the keys as compartment names such as 'class name', 'attributes', etc.
        - Grid -- The Node is positioned into this Grid
        - Compartments -- Each compartment to be filled in
        - Local_alignment -- Position of the node in the spanned area, vertical and horizontal
    """

    def __init__(self, node_type_name: str, content: List[List[str]], grid: 'Grid',
                 local_alignment: Optional[Alignment]):
        """
        Constructor

        :param node_type_name: A name such as class, state, imported class, etc
        :param content: A list of text blocks, each a list of text lines to be displayed in node Compartments
        :param grid: Reference to the Grid
        :param local_alignment: Overrides default alignment within Cell or Cell range
        """
        self.logger = logging.getLogger(__name__)
        self.Grid = grid
        try:
            self.Node_type = self.Grid.Diagram.Diagram_type.NodeTypes[node_type_name]
        except IndexError:
            raise UnsupportedNodeType(node_type_name=node_type_name,
                                      diagram_type_name=self.Grid.Diagram.Diagram_type.Name)

        # Create a list of compartments ordered top to bottom based on Node Type's Compartment Types
        self.Compartments = [Compartment(node=self, ctype=t, content=c) for t, c in
                             zip(self.Node_type.Compartment_types, content)]

        # The Node will be aligned in the Cell according to either the specified local alignment or, if none,
        # the default cell alignment that we got from the Diagram Layout Specification
        self.Local_alignment = local_alignment if local_alignment else diagram_layout.Default_cell_alignment

    @property
    def Canvas_position(self):
        """
        Must be overidden by each subclass.
        :return: None, None
        """
        return Position(x=None, y=None)

    @property
    def Size(self):
        """Adjust node size to accommodate text content in each compartment"""
        # For all compartments in this node, get the max height and width
        crects = [c.Text_block_size for c in self.Compartments]
        # Get the max of each compartment width and the default node type width
        # max_width = max([r.width for r in crects] + [self.Node_type.Default_size.width])
        max_width = max([r.width for r in crects])
        # Height is the sum of all compartment heights
        # Ignore the default node type height for now
        node_height = sum([r.height for r in crects])
        # Return a rectangle with the
        return Rect_Size(height=node_height, width=max_width)

    def Face_position(self, face: NodeFace):
        """
        Returns the position of the specified face on the x or y axis
        :param face : A node face
        :return: position in x or y
        """
        if face == NodeFace.TOP:
            return self.Canvas_position.y + self.Size.height
        elif face == NodeFace.BOTTOM:
            return self.Canvas_position.y
        elif face == NodeFace.RIGHT:
            return self.Canvas_position.x + self.Size.width
        else:
            return self.Canvas_position.x

    def render(self):
        """Calculate final position on the Canvas and register my rectangle in the Tablet"""

        self.logger.info("Drawing node")
        # Start at the bottom of the node and render each compartment upward
        comp_y = self.Canvas_position.y
        for c in self.Compartments[::-1]:  # Reverse the compartment order to bottom up
            c.render(Position(x=self.Canvas_position.x, y=comp_y))
            comp_y += c.Size.height  # bottom of next compartment is top of this one
