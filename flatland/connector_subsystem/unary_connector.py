"""
unary_connector.py
"""
import logging
from flatland.flatland_exceptions import UnsupportedConnectorType
from flatland.datatypes.command_interface import New_Stem
from flatland.connector_subsystem.anchored_stem import AnchoredStem
from flatland.connector_subsystem.connector import Connector
from flatland.connector_subsystem.connector_type import ConnectorType
from flatland.datatypes.connection_types import ConnectorName
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.diagram import Diagram


class UnaryConnector(Connector):
    """
    A single Stem is attached to the face of one Node. Supports initial and deletion pseudo-states on
    state machine diagrams, for example.
    """

    def __init__(self, diagram: 'Diagram', connector_type_name: str,
                 stem: New_Stem, name: Optional[ConnectorName]):
        """
        Constructor

        :param diagram: Reference to the Diagram
        :param connector_type_name: Name of the Connector Type
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating unary connector")
        # Verify that the specified connector type name corresponds to a supported connector type
        # found in our database
        try:
            ct = diagram.Diagram_type.ConnectorTypes[connector_type_name]
        except IndexError:
            raise UnsupportedConnectorType(
                connector_type_name=connector_type_name, diagram_type_name=diagram.Diagram_type.Name)
        super().__init__(diagram=diagram, name=name, connector_type=ct)

        unary_stem_type = self.Connector_type.Stem_type[stem.stem_type]
        anchor = stem.anchor if stem.anchor is not None else 0

        # Create the Unary Stem
        self.Unary_stem = AnchoredStem(
            connector=self,
            stem_type=unary_stem_type,
            semantic=stem.semantic,
            node=stem.node,
            face=stem.face,
            anchor_position=anchor,
            name=stem.stem_name
        )

    def render(self):
        """
        Draw the unary connector
        """
        layer = self.Diagram.Layer

        # Draw a line between the root end (on the node) and the vine end at the unary stem type's fixed distance
        layer.add_line_segment(
            asset=self.Connector_type.Name+' connector',
            from_here=self.Unary_stem.Root_end,
            to_there=self.Unary_stem.Vine_end
        )  # Symbols will be drawn on top of this line

        # Add stem decorations
        self.Unary_stem.render()

        if self.Name:
            # Not all connectors are named
            self.logger.info("Drawing connector name")
            name_position = self.compute_name_position(
                point_t=self.Unary_stem.Root_end, point_p=self.Unary_stem.Vine_end
            )
            layer.add_text_block(asset=self.Connector_type.Name + ' name', lower_left=name_position, text=self.Name.text)

