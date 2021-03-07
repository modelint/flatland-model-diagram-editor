"""
bending_binary_connector.py
"""
import logging
import logging.config
from flatland.flatland_exceptions import UnsupportedConnectorType, InvalidBendNumber
from flatland.connector_subsystem.binary_connector import BinaryConnector
from flatland.connector_subsystem.tertiary_stem import TertiaryStem
from flatland.connector_subsystem.anchored_stem import AnchoredStem
from flatland.datatypes.connection_types import HorizontalFace, Orientation, ConnectorName
from flatland.datatypes.geometry_types import Position
from flatland.datatypes.command_interface import New_Stem, New_Path
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.diagram import Diagram


class BendingBinaryConnector(BinaryConnector):
    """
    This is a Binary Connector that must turn one or more corners to connect its opposing Binary Stems.
    In such a case the two Binary Stems will be counterparts and we can arbitrarily start drawing a line
    from one of the Counterpart Binary Stems to the other. In fact, we could start from both ends and work
    toward the middle or start from the middle and work our way out. So the terms “start” and “end” could
    just as easily have been labeled “A” and “B”.
    """

    def __init__(self, diagram: 'Diagram', connector_type: str, anchored_stem_t: New_Stem,
                 anchored_stem_p: New_Stem, paths: Optional[New_Path] = None, name: Optional[ConnectorName] = None,
                 tertiary_stem: Optional[New_Stem] = None):
        """
        Constructor - see class description for meaning of the attributes

        :param diagram: Reference to the Diagram
        :param connector_type: Name of connector type
        :param anchored_stem_t: A user supplied specification of a stem with an anchored face placement
        :param anchored_stem_p: A user supplied specification of the opposing stem with an anchored face placement
        :param paths:
        :param name: User supplied name of the Connector
        :param tertiary_stem:
        """
        self.logger = logging.getLogger(__name__)
        # Verify that the specified connector type name corresponds to a supported connector type
        # found in our database
        try:
            ct = diagram.Diagram_type.ConnectorTypes[connector_type]
        except IndexError:
            raise UnsupportedConnectorType(
                connector_type_name=connector_type, diagram_type_name=diagram.Diagram_type.Name)
        BinaryConnector.__init__(self, diagram=diagram, name=name, connector_type=ct)

        # Paths are only necessary if the connector bends more than once
        self.Paths = paths if not None else []

        # Look up the stem types loaded from our database
        anchored_stem_t_type = self.Connector_type.Stem_type[anchored_stem_t.stem_type]
        anchored_stem_p_type = self.Connector_type.Stem_type[anchored_stem_p.stem_type]
        tertiary_stem_type = None
        if tertiary_stem:
            tertiary_stem_type = self.Connector_type.Stem_type[tertiary_stem.stem_type]

        # Create the two opposing Anchored Stems
        self.T_stem = AnchoredStem(
            connector=self,
            stem_type=anchored_stem_t_type,
            semantic=anchored_stem_t.semantic,
            node=anchored_stem_t.node,
            face=anchored_stem_t.face,
            anchor_position=anchored_stem_t.anchor if anchored_stem_t.anchor is not None else 0,
            name=anchored_stem_t.stem_name,
        )
        self.P_stem = AnchoredStem(
            connector=self,
            stem_type=anchored_stem_p_type,
            semantic=anchored_stem_p.semantic,
            node=anchored_stem_p.node,
            face=anchored_stem_p.face,
            anchor_position=anchored_stem_p.anchor if anchored_stem_p.anchor is not None else 0,
            name=anchored_stem_p.stem_name,
        )
        self.Corners = self.compute_corners()

        self.Tertiary_stem = None
        if tertiary_stem:
            # Find all line segments in the bending connector parallel to the tertiary node face
            # Where the tertiary stem is attached
            points = [self.T_stem.Vine_end] + self.Corners + [self.P_stem.Vine_end]
            segs = set(zip(points, points[1:]))
            horizontal_segs = {s for s in segs if s[0].y == s[1].y}
            parallel_segs = horizontal_segs if tertiary_stem.face in HorizontalFace else segs - horizontal_segs
            self.Tertiary_stem = TertiaryStem(
                connector=self,
                stem_type=tertiary_stem_type,
                semantic=tertiary_stem.semantic,
                node=tertiary_stem.node,
                face=tertiary_stem.face,
                anchor_position=tertiary_stem.anchor if tertiary_stem.anchor is not None else 0,
                name=tertiary_stem.stem_name,
                parallel_segs=parallel_segs
            )

    def compute_corners(self) -> List[Position]:
        if not self.Paths:  # Only one corner
            return [self.node_to_node()]
        else:
            corners = []
            to_horizontal_path = self.T_stem.Node_face in HorizontalFace
            first_path = True
            for p in self.Paths:
                if to_horizontal_path:  # Row
                    self.Diagram.Grid.add_lane(lane=p.lane, orientation=Orientation.Horizontal)
                    previous_x = self.T_stem.Vine_end.x if first_path else corners[-1].x
                    rut_y = self.Diagram.Grid.get_rut(lane=p.lane, rut=p.rut, orientation=Orientation.Horizontal)
                    x, y = previous_x, rut_y
                else:  # Column
                    self.Diagram.Grid.add_lane(lane=p.lane, orientation=Orientation.Vertical)
                    previous_y = self.T_stem.Vine_end.y if first_path else corners[-1].y
                    rut_x = self.Diagram.Grid.get_rut(lane=p.lane, rut=p.rut, orientation=Orientation.Vertical)
                    x, y = rut_x, previous_y
                corners.append(Position(x, y))
                to_horizontal_path = not to_horizontal_path  # toggle the orientation
                first_path = False
            # Cap final path with last corner
            if to_horizontal_path:
                x = corners[-1].x
                y = self.P_stem.Vine_end.y
            else:
                x = self.P_stem.Vine_end.x
                y = corners[-1].y
            corners.append(Position(x, y))
            return corners

    def node_to_node(self) -> Position:
        """
        Create a single corner between two Nodes
        :return: Corner
        """
        if self.T_stem.Node_face in HorizontalFace:
            corner_x = self.T_stem.Root_end.x
            corner_y = self.P_stem.Root_end.y
        else:
            corner_x = self.P_stem.Root_end.x
            corner_y = self.T_stem.Root_end.y

        return Position(corner_x, corner_y)

    def render(self):
        """
        Draw a line from the vine end of the T node stem to the vine end of the P node stem
        """
        # Create line from root end of T_stem to root end of P_stem, bending along the way
        self.logger.info("Drawing bending binary connector")
        layer = self.Diagram.Layer
        layer.add_open_polygon(
            asset=self.Connector_type.Name+' connector',
            vertices=[self.T_stem.Root_end] + self.Corners + [self.P_stem.Root_end]
        )
        # Draw the stems and their decorations
        self.T_stem.render()
        self.P_stem.render()
        if self.Tertiary_stem:
            self.Tertiary_stem.render()

        # Draw the connector name if any
        bend = self.Name.bend  # Name will be centered relative to this user requested bend
        max_bend = len(self.Corners)+1
        if not 1 <= bend <= max_bend:
            raise InvalidBendNumber(bend, max_bend)
        # Bends are numbered starting at 1 from the user designated T node
        # Point T (closest to the T Node) is T stem's root end if the first bend is requested, otherwise a corner
        point_t = self.T_stem.Root_end if bend == 1 else self.Corners[bend-2]  # Bend 2 gets the first corner at index 0
        # Point P (closest to the P Node) is P stem's root end if the bend is one more than the number of Corners
        # If there is only a single corner and bend is 2, use the P stem root end
        # If there are two corners and the bend is 2, use the Corner at index 1 (2nd corner)
        point_p = self.P_stem.Root_end if bend == len(self.Corners)+1 else self.Corners[bend-1]
        name_position = self.compute_name_position(point_t, point_p)
        layer.add_text_line(asset=self.Connector_type.Name + ' name', lower_left=name_position, text=self.Name.text)
