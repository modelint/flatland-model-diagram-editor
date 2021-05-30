""" compartment.py """

from flatland.datatypes.geometry_types import Rect_Size, Position, HorizAlign, VertAlign
from flatland.datatypes.command_interface import New_Compartment
from typing import TYPE_CHECKING, List
from flatland.node_subsystem.node_type import CompartmentType

if TYPE_CHECKING:
    from flatland.node_subsystem.node import Node


class Compartment:
    """
    A rectangle filled with text inside of a Node

        Attributes

        - Name -- Compartment type name indicating overall purpose of compartment (Title, Attributes, Methods, etc)
        - Alignment -- Alignment of text block within the compartment
        - Padding -- Extra space between text block and Node boundary
        - Text style -- Font, size, etc of text
    """

    def __init__(self, node: 'Node', ctype: CompartmentType, spec: New_Compartment):
        """
        Constructor

        :param node: Node reference - Compartment is inside this Node
        :param ctype: Compartment Type referende - Specifies layout and stack order of this Compartment
        :param content: Text block a list of text lines to be rendered inside this Compartment
        :param expansion: After fitting text, expand the height of this node by this factor
        """
        self.Type = ctype
        self.Node = node
        self.Content = spec.content  # list of text lines
        self.Expansion = spec.expansion

    @property
    def Text_block_size(self) -> Rect_Size:
        """Compute the size of the text block with required internal compartment padding"""
        layer = self.Node.Grid.Diagram.Layer
        asset = ' '.join([self.Node.Node_type.Name, self.Type.name])
        unpadded_text_size = layer.text_block_size(asset=asset, text_block=self.Content)

        # Now add the padding specified for this compartment type
        padded_text_width = unpadded_text_size.width + self.Type.padding.left + self.Type.padding.right
        padded_text_height = unpadded_text_size.height + self.Type.padding.top + self.Type.padding.bottom
        return Rect_Size(width=padded_text_width, height=padded_text_height)

    @property
    def Size(self) -> Rect_Size:
        """Compute the size of the visible border"""
        # Width matches the node width and the height is the full text block size
        expanded_height = self.Text_block_size.height + self.Text_block_size.height * self.Expansion
        return Rect_Size(width=self.Node.Size.width, height=expanded_height)

    def render(self, lower_left_corner: Position):
        """Create rectangle on the tablet and add each line of text"""
        layer = self.Node.Grid.Diagram.Layer
        # Asset name could be 'state activity compartment' or 'class attributes compartment' for example

        asset = ' '.join([self.Node.Node_type.Name, self.Type.name, 'compartment'])
        layer.add_rectangle(asset=asset, lower_left=lower_left_corner, size=self.Size, color_usage=self.Node.Tag)

        # Horizontal alignment of text block relative to its compartment by calculating lower left x position
        if self.Type.halign == HorizAlign.LEFT:
            xpos = lower_left_corner.x + self.Type.padding.left
        elif self.Type.halign == HorizAlign.CENTER:
            xpos = lower_left_corner.x + self.Type.padding.left + \
                   (self.Size.width / 2) - (self.Text_block_size.width / 2)
        elif self.Type.halign == HorizAlign.RIGHT:
            xpos = lower_left_corner.x + self.Type.padding.left + \
                   (self.Size.width - self.Type.padding.right - self.Text_block_size.width)
        else:
            assert False, "Illegal value for horizontal compartment alignment"

        # Vertical alignment of text block relative to its compartment
        if self.Type.valign == VertAlign.TOP:
            ypos = lower_left_corner.y + self.Size.height - self.Text_block_size.height + self.Type.padding.bottom
        elif self.Type.valign == VertAlign.CENTER:
            ypos = lower_left_corner.y + (self.Size.height / 2) - \
                   (self.Text_block_size.height-self.Type.padding.top-self.Type.padding.bottom)/2
        elif self.Type.valign == VertAlign.BOTTOM:
            ypos = lower_left_corner.y + self.Type.padding.bottom
        else:
            assert False, "Illegal value for vertical compartment alignment"

        text_position = Position(xpos, ypos)
        asset = ' '.join([self.Node.Node_type.Name, self.Type.name])
        layer.add_text_block(asset=asset, lower_left=text_position, text=self.Content,
                             align=self.Type.halign)
