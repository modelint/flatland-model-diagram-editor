"""
branch.py
"""
import logging
from typing import Set, TYPE_CHECKING
from flatland.connector_subsystem.anchored_tree_stem import AnchoredTreeStem
from flatland.datatypes.geometry_types import Line_Segment, Position, Coordinate
from flatland.datatypes.connection_types import Orientation
from flatland.datatypes.general_types import Index

if TYPE_CHECKING:
    from flatland.connector_subsystem.tree_connector import TreeConnector


class Branch:
    def __init__(self, order: Index, axis: Coordinate, connector: 'TreeConnector', hanging_stems: Set[AnchoredTreeStem],
                 axis_orientation: Orientation):
        """
        Constructor

        :param order:
        :param axis:
        :param connector:
        :param hanging_stems:
        :param axis_orientation:
        """
        self.logger = logging.getLogger(__name__)
        self.Order = order
        self.Connector = connector
        self.Hanging_stems = hanging_stems
        self.Axis = axis
        self.Axis_orientation = axis_orientation

    @property
    def Shoot(self) -> Line_Segment:
        branches = self.Connector.Branches
        prev_axis = None if self.Order == 0 else branches[self.Order - 1].Axis
        next_axis = None if self.Order == len(branches) - 1 else branches[self.Order + 1].Axis
        positions = {a for a in {prev_axis, next_axis} if a}
        if self.Axis_orientation == Orientation.Horizontal:
            y = self.Axis
            positions = positions.union({s.Root_end.x for s in self.Hanging_stems})
            x1 = min(positions)
            x2 = max(positions)
            return Line_Segment(from_position=Position(x1, y), to_position=Position(x2, y))
        else:
            x = self.Axis
            positions = positions.union({s.Root_end.y for s in self.Hanging_stems})
            y1 = min(positions)
            y2 = max(positions)
        return Line_Segment(from_position=Position(x, y1), to_position=Position(x, y2))

    def render(self):
        layer = self.Connector.Diagram.Layer

        # Draw the axis
        layer.add_line_segment(
            asset=self.Connector.Connector_type.Name+' connector',
            from_here=self.Shoot.from_position, to_there=self.Shoot.to_position
        )

        # Draw the stems
        for s in self.Hanging_stems:
            if self.Axis_orientation == Orientation.Horizontal:
                x = s.Root_end.x
                y = self.Axis
            else:
                x = self.Axis
                y = s.Root_end.y

            self.logger.info("Drawing branch stem")
            layer.add_line_segment(
                asset=self.Connector.Connector_type.Name+' connector', from_here=s.Root_end, to_there=Position(x, y)
            )
