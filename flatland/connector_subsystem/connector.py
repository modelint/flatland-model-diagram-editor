"""
connector.py - Covers the Connector class in the Flatland3 Connector Subsystem Class Diagram
"""
from flatland.flatland_exceptions import InvalidNameSide
from flatland.connector_subsystem.connector_type import ConnectorType
from flatland.datatypes.connection_types import ConnectorName
from flatland.datatypes.geometry_types import Rect_Size, Position
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.diagram import Diagram


class Connector:
    """
    A Connector is a set of Stems connected by one or more lines to form a contiguous branch bringing
    one or more Nodes into a drawn model level relationship. On a class diagram, for example, a Connector
    is drawn for each binary association, generalization and association class relationship.

    The Connector Type and its Stem Types determine how the Connector should be drawn.

        Attributes

        - Diagram -- Connector is drawn on this diagram
        - Connector_type -- Specifies characteristics of this Connector
        - Name -- Optional name of this Connector
    """

    def __init__(self, diagram: 'Diagram', name: Optional[ConnectorName], connector_type: ConnectorType):
        """
        Constructor

        :param diagram: Reference to the Diagram
        :param connector_type: Name of this Connector Type
        """
        self.Diagram = diagram
        self.Connector_type = connector_type
        self.Name = name
        self.Name_size = None
        if self.Name:
            if self.Name.side not in {1, -1}:
                raise InvalidNameSide(self.Name.side)
            layer = self.Diagram.Layer
            # Get size of bounding box
            self.Name_size = layer.text_block_size(
                asset=self.Connector_type.Name + ' name', text_block=[self.Name.text]
            )

        self.Diagram.Grid.Connectors.append(self)

    def compute_name_position(self, point_t: Position, point_p: Position) -> Position:
        """
        Determine the lower left corner position of this Connector's name

        :param point_t: Point closest to the T Node
        :param point_p: Point closest to the P Node (furthest from the T Node)
        :return: Position of name bounding box lower left corner
        """
        name_spec = self.Connector_type.Name_spec  # For easy access below
        if point_t.y == point_p.y:
            # Bend is horizontal
            center_x = round(abs(point_t.x - point_p.x) / 2) + min(point_t.x, point_p.x)  # Distance type is an integer
            name_x = center_x - round(self.Name_size.width / 2)
            # If box is below the connector, subtract the height of the box as well to get lower left corner y
            height_offset = self.Name_size.height if self.Name.side == -1 else 0
            name_y = point_t.y + name_spec.axis_buffer.vertical * self.Name.side - height_offset
            #  TODO: Above line doesn't look right, also adapt to use end buffer
        else:
            # Connector is vertical
            center_y = round(abs(point_t.y - point_p.y) / 2) + min(point_t.y, point_p.y)
            name_y = center_y - round(self.Name_size.height / 2)
            # If box is left of the connector, subtract the width of the box as well to get the lower left corner x
            width_offset = self.Name_size.width if self.Name.side == -1 else 0
            name_x = point_t.x + name_spec.axis_buffer.horizontal * self.Name.side - width_offset
        return Position(name_x, name_y)

    def render(self):
        pass  # overriden

    def __repr__(self):
        return f'ID: {id(self)}, Diagram: {self.Diagram}, Type: {self.Connector_type.Name}, Name: {self.Name}'
