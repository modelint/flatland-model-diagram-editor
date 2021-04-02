""" spanning_node.py """

from flatland.flatland_exceptions import BadColNumber, BadRowNumber, BadRowSpan, BadColSpan
from flatland.node_subsystem.node import Node
from flatland.datatypes.geometry_types import Position, Alignment
from flatland.geometry_domain.linear_geometry import align_on_axis
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from flatland.node_subsystem.grid import Grid

class SpanningNode(Node):
    """
    A node that spans multiple rows and/or columns. On a class diagram this is useful for positioning
    a superclass above two subclasses. The superclass spans two columns each containing a subclass.

    The simplest case of a span involves just one column and one row. But it is best to specify that as
    a single cell node.  But it would be common to specify a spanning node only across rows or columns.
    Only a particularly large node would need both rows and columns.

    Note that a cell may contain at most one Node. So if a node spans into some cell, no other Node may be placed
    in that Cell even if the Node isn't large enough to intrude into the Cell area.  Therefore, the modeler
    must take care to not specify too large an area to span relative to the actual Node size.

    Attributes
    ---
    Low_row : The lowest row
    High_row : The topmost row
    Left_column : The leftmost column
    Right_column : The rightmost column
    """
    def __init__(self, node_type_name: str, content: List[List[str]], grid: 'Grid',
                 low_row: int, high_row: int, left_column: int, right_column: int,
                 local_alignment: Optional[Alignment] = None):
        super().__init__(node_type_name, content, grid, local_alignment)
        # Validate the span
        if low_row <= 0:
            raise BadRowNumber
        if left_column <= 0:
            raise BadColNumber
        if not (high_row >= low_row >= 0):
            raise BadRowSpan
        if not (right_column >= left_column >= 0):
            raise BadColSpan

        self.High_row = high_row
        self.Low_row = low_row
        self.Left_column = left_column
        self.Right_column = right_column
        self.Grid.place_spanning_node(node=self)

    def __repr__(self):
        return f'{self.Compartments[0].Content}[R{self.Low_row}-{self.High_row}, C{self.Left_column}-{self.Right_column}]'

    def __str__(self):
        return f'Grid [{self.Low_row}-{self.High_row}, {self.Left_column}-{self.Right_column}] @ ({round(self.Canvas_position.x, 2)}, ' \
               f'{round(self.Canvas_position.y, 2)}), W {round(self.Size.width, 2)} x H {round(self.Size.height, 2)}'

    @property
    def Canvas_position(self):
        """Position of lower left corner on the Canvas"""
        # Workout alignment within Cell
        lower_left_x = align_on_axis(
            axis_alignment=self.Local_alignment.horizontal.value,
            boundaries=self.Grid.Col_boundaries, from_grid_unit=self.Left_column, to_grid_unit=self.Right_column,
            from_padding=self.Grid.Cell_padding.left, to_padding=self.Grid.Cell_padding.right,
            node_extent=self.Size.width
        ) + self.Grid.Diagram.Origin.x # +  self.Grid.Col_boundaries[self.Column-1]
        lower_left_y = align_on_axis(
            axis_alignment=self.Local_alignment.vertical.value,
            boundaries=self.Grid.Row_boundaries, from_grid_unit=self.Low_row, to_grid_unit=self.High_row,
            from_padding=self.Grid.Cell_padding.bottom, to_padding=self.Grid.Cell_padding.top,
            node_extent=self.Size.height
        ) + self.Grid.Diagram.Origin.y # + self.Grid.Row_boundaries[self.Row-1]
        return Position(x=lower_left_x, y=lower_left_y)

