""" single_cell_node.py """

from flatland.flatland_exceptions import BadColNumber, BadRowNumber
from flatland.geometry_domain.linear_geometry import align_on_axis
from flatland.node_subsystem.node import Node
from flatland.datatypes.geometry_types import Position, Alignment

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.grid import Grid


class SingleCellNode(Node):
    """
    A node enveloped by a single Cell

        Attributes

        - row -- Placed in this row
        - column -- Placed at this column
    """
    def __init__(self, node_type_name: str, content: List[List[str]], grid: 'Grid', row: int, column: int,
                 local_alignment: Optional[Alignment] = None):
        """
        Constructor

        :param node_type_name:
        :param content:
        :param grid:
        :param row:
        :param column:
        :param local_alignment:
        """
        Node.__init__(self, node_type_name, content, grid, local_alignment)
        if row <= 0:
            raise BadRowNumber
        if column <= 0:
            raise BadColNumber
        self.Row = row
        self.Column = column
        self.Grid.place_single_cell_node(node=self)

    def __repr__(self):
        return f'{self.Compartments[0].Content}[R{self.Row}, C{self.Column}]'

    def __str__(self):
        return f'Grid [{self.Row}, {self.Column}] @ ({round(self.Canvas_position.x, 2)}, ' \
               f'{round(self.Canvas_position.y, 2)}), W {round(self.Size.width, 2)} x H {round(self.Size.height, 2)}'

    @property
    def Canvas_position(self):
        """Position of lower left corner on the Canvas"""
        # Workout alignment within Cell
        lower_left_x = align_on_axis(
            axis_alignment=self.Local_alignment.horizontal.value,
            boundaries=self.Grid.Col_boundaries, from_grid_unit=self.Column, to_grid_unit=self.Column,
            from_padding=self.Grid.Cell_padding.left, to_padding=self.Grid.Cell_padding.right,
            node_extent=self.Size.width
        ) + self.Grid.Diagram.Origin.x  # +  self.Grid.Col_boundaries[self.Column-1]
        lower_left_y = align_on_axis(
            axis_alignment=self.Local_alignment.vertical.value,
            boundaries=self.Grid.Row_boundaries, from_grid_unit=self.Row, to_grid_unit=self.Row,
            from_padding=self.Grid.Cell_padding.bottom, to_padding=self.Grid.Cell_padding.top,
            node_extent=self.Size.height
        ) + self.Grid.Diagram.Origin.y  # + self.Grid.Row_boundaries[self.Row-1]
        return Position(lower_left_x, lower_left_y)
