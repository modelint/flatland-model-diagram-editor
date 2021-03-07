"""
stem.py
"""

from flatland.flatland_exceptions import InvalidNameSide, OutofDiagramBounds
from flatland.connector_subsystem.stem_type import StemType
from flatland.datatypes.geometry_types import Position, HorizAlign
from flatland.connector_subsystem.rendered_symbol import RenderedSymbol
from flatland.datatypes.connection_types import NodeFace, StemName

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from connector import Connector
    from node import Node


class Stem:
    """
    This is a line drawn from a face on a Node outward. The terminator on the node face is the root and the
    terminator on the other side of the line is the vine. A Stem may be decorated on either, both or neither end.
    A decoration consists of a graphic symbol such as an arrowhead or a circle or a fixed text label such as the
    UML '0..1' multiplicity label. A graphic symbol may be combined with a text symbol such as the Shlaer-Mellor
    arrow head 'c' conditionality combination.

        Attributes

        - Connector -- Stem is on one end of this Connector
        - Stem_type -- Specifies charactersitics and decoration, if any, of this Stem
        - Node -- Stem is attached to this Node
        - Node_face -- On this face of the Node
        - Root_end -- Where the Stem attaches to the Node face
        - Vine_end -- End of Stem away from Node face with clearance for any decoration

        Relationships

        - Root_rendered_symbol -- R61/Rendered Symbol
        - Vine_rendered_symbol -- R61/Rendered Symbol
        - Stem_name -- R73/Stem Name
    """

    def __init__(self, connector: 'Connector', stem_type: StemType, semantic: str, node: 'Node',
                 face: NodeFace, root_position: Position, name: Optional[StemName]):
        self.Connector = connector
        self.Stem_type = stem_type
        self.Node = node
        self.Node_face = face
        self.Semantic = semantic
        self.Root_end = root_position
        self.Name = name
        self.Name_size = None  # Computed below if name was specified
        self.Leading = None  # TODO: This and next attr needs to go into an add text block function in tablet
        self.Line_height = None
        if self.Name:
            if self.Name.side not in {1, -1}:
                raise InvalidNameSide(self.Name.side)
            layer = self.Connector.Diagram.Layer
            # Get size of name bounding box
            self.Name_size = layer.text_block_size(asset=self.Stem_type.Name + ' name', text_block=self.Name.text.text)

        # There are at most two rendered symbols (one on each end) of a Stem and usually none or one
        self.Root_rendered_symbol = None  # Default assumption until lookup a bit later
        self.Vine_rendered_symbol = None

        # Some stem subclasses will compute their vine end, but for a fixed geometry, we can do it right here
        if self.Stem_type.Geometry == 'fixed':
            # For a fixed geometry, the Vine end is a fixed distance from the Root End
            stem_len = self.Stem_type.Minimum_length
            # Compute the coordinates based on the stem direction using the rooted node face
            x, y = self.Root_end
            if face == NodeFace.RIGHT:
                x = x + stem_len
            elif face == NodeFace.LEFT:
                x = x - stem_len
            elif face == NodeFace.TOP:
                y = y + stem_len
            elif face == NodeFace.BOTTOM:
                y = y - stem_len
            self.Vine_end = Position(x, y)
        # TODO: consider Free geometry

    def render(self):
        """
        Draw a symbol at the root, vine, both or neither end of this Stem
        """
        layer = self.Connector.Diagram.Layer

        if self.Name:
            align = HorizAlign.LEFT  # Assume left alignment of text lines
            name_spec = self.Stem_type.Name_spec
            if self.Vine_end.y == self.Root_end.y:
                # Horizontal stem
                if self.Node_face == NodeFace.LEFT:
                    align = HorizAlign.RIGHT  # Text is to the left of node face, so right align it
                    width_offset = -(self.Name_size.width + name_spec.end_buffer.horizontal)
                else:
                    width_offset = name_spec.end_buffer.horizontal
                name_x = self.Root_end.x + width_offset
                height_offset = self.Name_size.height if self.Name.side == -1 else 0
                name_y = self.Root_end.y + (name_spec.axis_buffer.vertical + height_offset) * self.Name.side
            else:
                # Vertical stem
                if self.Name.side == -1:  # Text is to the left of vertical stem, so right align it
                    align = HorizAlign.RIGHT
                if self.Node_face == NodeFace.BOTTOM:
                    height_offset = -(self.Name_size.height + name_spec.end_buffer.vertical)
                else:
                    height_offset = name_spec.end_buffer.vertical
                name_y = self.Root_end.y + height_offset
                width_offset = self.Name_size.width if self.Name.side == -1 else 0
                name_x = self.Root_end.x + (name_spec.axis_buffer.horizontal + width_offset) * self.Name.side

            diagram = self.Connector.Diagram
            if name_x < diagram.Origin.x or \
                    name_x > diagram.Canvas.Size.width - diagram.Padding.right or \
                    name_y < diagram.Origin.y or \
                    name_y > diagram.Canvas.Size.height - diagram.Padding.top:
                raise OutofDiagramBounds(object_type='text block', x_value=name_x, y_value=name_y)

            layer.add_text_block(asset=self.Stem_type.Name + ' name', lower_left=Position(name_x, name_y),
                                  text=self.Name.text.text, align=align)

        root_symbol_name = self.Stem_type.DecoratedStems[self.Semantic].Root_symbol
        vine_symbol_name = self.Stem_type.DecoratedStems[self.Semantic].Vine_symbol

        if root_symbol_name:
            self.Root_rendered_symbol = RenderedSymbol(
                stem=self,
                end='root', location=self.Root_end,
                symbol_name=root_symbol_name
            )
        if vine_symbol_name:
            self.Vine_rendered_symbol = RenderedSymbol(
                stem=self,
                end='vine', location=self.Vine_end,
                symbol_name=vine_symbol_name
            )
