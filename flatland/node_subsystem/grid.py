"""
grid.py
"""

import logging
from flatland.flatland_exceptions import CellOccupiedFE, SheetWidthExceededFE, SheetHeightExceededFE
from flatland.connector_subsystem.connector_layout_specification import ConnectorLayoutSpecification as connector_layout
from flatland.node_subsystem.diagram_layout_specification import DiagramLayoutSpecification as diagram_layout
from flatland.geometry_domain.linear_geometry import expand_boundaries, span, step_edge_distance
from flatland.datatypes.geometry_types import Position, Rect_Size
from flatland.node_subsystem.spanning_node import SpanningNode
from flatland.node_subsystem.single_cell_node import SingleCellNode
from flatland.datatypes.connection_types import Orientation
from itertools import product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.node_subsystem.diagram import Diagram

show_grid = True


class Grid:
    """
    Positioning nodes in a drawing tool typically involves pixel level placement which
    is overkill for most types of model drawings. To get straight lines you need to fidget
    the pixel level position and alignment. Some tools let you snap to a grid, but the grid
    is usually fine grained to make it possible to position the node connectors.

    In Flatland, we use a single Grid laid out across a Canvas like a spreadsheet. Rows and
    Columns in the Grid can be any width, but are generally small, medium or large node-sized.
    In a class diagram, for example, each Column is roughly the size of one class-width and each Row
    is roughly the height of a single class-height. This makes it easy to specify position using
    a text markup language. Each Node is placed at a grid coordinate with a default or specified alignment.
    For particularly large nodes, you can position them on a single Cell of the Grid and then have
    them span multiple Rows or Columns.

    So the Grid defines a coordinate system for the placement of Nodes.

    It starts out empty, with no Rows or Columns and only an origin. Each loaded Node specifies a desired
    placement coordinate. The Grid then extends by the necessary (if any) Rows and Columns to create a place
    to position the Node.

        Attributes

        - Cells -- 2D array of Nodes, initially empty
        - Nodes -- All the nodes on the grid in placement order
        - Row_boundaries -- Floor y of each row ascending upward
        - Col_boundaries -- Left side x of each column, ascending rightward
        - Cell_padding -- Distances from cell to drawn node boundaries
        - Cell_alignment -- Default alignment for any placed node (can be overidden locally by node)
        - Diagram -- The Diagram that this Grid organizes content of
    """

    def __init__(self, diagram: 'Diagram', show: bool = False):
        """
        Constructor

        :param diagram:  Reference to the Diagram
        """
        self.logger = logging.getLogger(__name__)
        self.Cells = []  # No rows or columns in grid yet
        self.Nodes = []  # No nodes in the grid yet
        self.Connectors = []
        self.Row_boundaries = [0]
        self.Col_boundaries = [0]
        self.Cell_padding = diagram_layout.Default_cell_padding
        self.Cell_alignment = diagram_layout.Default_cell_alignment
        self.Diagram = diagram
        self.Show = show

    def __repr__(self):
        return f'Cells: {self.Cells}, Row boundaries: {self.Row_boundaries}, Col boundaries: {self.Col_boundaries}' \
               f'Cell padding: {self.Cell_padding}, Cell alignment: {self.Cell_alignment}'

    def get_rut(self, lane: int, rut: int, orientation: Orientation) -> int:
        """
        Compute a y coordinate above row boundary if lane_orientation is row
        or an x coordinate right of column boundary if lane_orientation is column
        :param: lane,
        :param: orientation
        :return: rut_position
        """
        if orientation == Orientation.Horizontal:
            # TODO: Consider expressing row/column boundaries in Canvas coordinates so this offset is not needed
            origin_offset = self.Diagram.Origin.y  # Boundaries are relative to the Diagram origin
            low_boundary = self.Row_boundaries[lane - 1]
            lane_width = self.Row_boundaries[lane] - low_boundary
        else:
            origin_offset = self.Diagram.Origin.x
            low_boundary = self.Col_boundaries[lane - 1]
            lane_width = self.Col_boundaries[lane] - low_boundary

        return origin_offset + low_boundary + step_edge_distance(
            num_of_steps=connector_layout.Default_rut_positions, extent=lane_width, step=rut)

    def render(self):
        """
        Draw Grid on Tablet for diagnostic purposes
        """

        if self.Show:
            grid_layer = self.Diagram.Canvas.Tablet.layers['grid']
            self.logger.info("Drawing grid")
            # Draw rows
            left_extent = self.Diagram.Origin.x
            right_extent = self.Diagram.Origin.x + self.Diagram.Size.width
            for r, h in enumerate(self.Row_boundaries):
                grid_layer.add_line_segment(asset='row boundary',
                                            from_here=Position(left_extent, h + self.Diagram.Origin.y),
                                            to_there=Position(right_extent, h + self.Diagram.Origin.y)
                                            )
                grid_layer.add_text_line(asset='grid label',
                                         lower_left=Position(left_extent - 20, self.Diagram.Origin.y + h + 30),
                                         text=str(r + 1))

            # Draw columns
            bottom_extent = self.Diagram.Origin.y
            top_extent = bottom_extent + self.Diagram.Size.height
            for c, w in enumerate(self.Col_boundaries):
                grid_layer.add_line_segment(asset='column boundary',
                                            from_here=Position(w + self.Diagram.Origin.x, bottom_extent),
                                            to_there=Position(w + self.Diagram.Origin.x, top_extent)
                                            )
                grid_layer.add_text_line(asset='grid label',
                                         lower_left=Position(w + self.Diagram.Origin.x + 30, bottom_extent - 20),
                                         text=str(c + 1))

            # Draw diagram boundary
            grid_layer.add_rectangle(asset='grid boundary',
                                     lower_left=Position(x=self.Diagram.Origin.x, y=self.Diagram.Origin.y),
                                     size=self.Diagram.Size)

        # Draw nodes
        [n.render() for n in self.Nodes]

        # Draw connectors
        [c.render() for c in self.Connectors]

    def add_row(self, cell_height):
        """Adds an empty row upward with the given height"""
        # Compute the new y position relative to the Diagram y origin
        new_row_height = self.Row_boundaries[-1] + cell_height
        # Make sure that it's not above the Diagram area
        if new_row_height > self.Diagram.Size.height:
            raise SheetHeightExceededFE
        # Add it to the list of row boundaries
        self.Row_boundaries.append(new_row_height)
        # Create new empty row with an empty node for each column boundary after the leftmost edge (0)
        empty_row = [None for _ in self.Col_boundaries[1:]]
        # Add it to our list of rows
        self.Cells.append(empty_row)

    def add_column(self, cell_width):
        """Adds an empty column rightward with the given width"""
        # Compute the new rightmost column boundary x value
        new_col_width = self.Col_boundaries[-1] + cell_width
        # Make sure that it's not right of the Diagram area
        if new_col_width > self.Diagram.Size.width:
            raise SheetWidthExceededFE
        # Add it to the list of column boundaries
        self.Col_boundaries.append(new_col_width)
        # For each row, add a rightmost empty node space
        [row.append(None) for row in self.Cells]

    def place_spanning_node(self, node: SpanningNode):
        """Places a spanning node adding any required rows or columns"""

        # Get the top and right extents for the grid
        # The top row or rightmost col number = qty of boundaries exluding 0 on y or x
        highest_row_number = max(0, len(self.Row_boundaries[1:]))
        rightmost_col_number = max(0, len(self.Col_boundaries[1:]))

        # Determine how many total rows and columns required to extend the grid
        # So that the node can be placed
        # We get zero if we already have all the rows and columns we need
        total_rows_to_add = max(0, node.High_row - highest_row_number)
        total_cols_to_add = max(0, node.Right_column - rightmost_col_number)

        # Which of these added rows and columns will be occupied by this node
        row_span = 1 + node.High_row - node.Low_row  # Number of rows this node will span
        col_span = 1 + node.Right_column - node.Left_column  # Number of cols this node will span

        # Some of the inserted rows and columns will not be spanned by the node
        # If you have an empty grid to start, for example, and you want to insert
        # a fat node across cols 1-2 in row 2, only row 2 is spanned with row 1 inserted
        # as an empty spacer row
        spacer_rows_to_add = max(0, (total_rows_to_add - row_span))
        spacer_cols_to_add = max(0, (total_cols_to_add - col_span))

        # Which rows or columns that already exist in the grid lie within the
        # specified node spanning range?
        spanned_existing_rows = list(range(node.Low_row, min(node.High_row, highest_row_number)))
        spanned_existing_cols = list(range(node.Left_column, min(node.Right_column, rightmost_col_number)))
        # spanned_existing_rows = list(range(node.Low_row, node.High_row + 1))
        # spanned_existing_cols = list(range(node.Left_column, node.Right_column + 1))

        # Now take all existing cells in the occupied area and ensure that each is empty
        if spanned_existing_rows and spanned_existing_cols:
            # We subtract 1 to get from canvas row col coordinates to grid cell indices
            occupied_cells = [self.Cells[r - 1][c - 1] for r, c in
                              product(spanned_existing_rows, spanned_existing_cols)]
            if any(occupied_cells):
                raise CellOccupiedFE

        # Add cell padding to the node to determine grid space required
        padded_node_height = node.Size.height + self.Cell_padding.top + self.Cell_padding.bottom
        padded_node_width = node.Size.width + self.Cell_padding.left + self.Cell_padding.right

        # How much of the padded node height is accommodated by existing rows?
        top_boundary = self.Row_boundaries[-1]  # topmost y of grid
        bottom_boundary = self.Row_boundaries[-len(spanned_existing_rows) - 1]  # floor boundary of lowest spanned node
        overlapped_height = top_boundary - bottom_boundary

        # How much of the padded node width is accommodated by existing columns?
        right_boundary = self.Col_boundaries[-1]  # rightmost x of grid
        left_boundary = self.Col_boundaries[-len(spanned_existing_cols) - 1]  # left boundary of leftmost spanned node
        overlapped_width = right_boundary - left_boundary

        # How much height would be added by default size extra rows?
        default_cell_height = node.Node_type.Default_size.height + self.Cell_padding.top + self.Cell_padding.bottom
        default_added_height = row_span * default_cell_height  # Height that would be added by default
        surplus_height = max(0, padded_node_height - overlapped_height - default_added_height)  # Surplus required
        insert_more_height_per_new_cell = 0  # Amount of height to add to each newly created row
        if surplus_height:
            insert_more_height_per_new_cell += surplus_height / row_span
        cell_height = default_cell_height + insert_more_height_per_new_cell

        # How much width would be added by default size extra columns?
        default_cell_width = node.Node_type.Default_size.width + self.Cell_padding.left + self.Cell_padding.right
        default_added_width = col_span * default_cell_width  # Width that would be added by default
        surplus_width = max(0, padded_node_width - overlapped_width - default_added_width)  # Surplus required
        insert_more_width_per_new_cell = 0  # Amount of width to add to each newly created column
        if surplus_width:
            insert_more_width_per_new_cell += surplus_width / col_span
        cell_width = default_cell_width + insert_more_width_per_new_cell

        # Add any required spacer rows and columns first, setting them to the default
        # node height and width
        [self.add_row(default_cell_height) for _ in range(spacer_rows_to_add)]
        [self.add_column(default_cell_width) for _ in range(spacer_cols_to_add)]

        # Now we add rows and columns that will actually be spanned by the node
        # These are sized based on the space required to accommodate this node
        [self.add_row(cell_height) for _ in range(total_rows_to_add - spacer_rows_to_add)]
        [self.add_column(cell_width) for _ in range(total_cols_to_add - spacer_cols_to_add)]

        # Assign each cell to this node
        spanned_rows = list(range(node.Low_row, node.High_row + 1))
        spanned_cols = list(range(node.Left_column, node.Right_column + 1))
        for r, c in product(spanned_rows, spanned_cols):
            self.Cells[r - 1][c - 1] = node
        self.Nodes.append(node)

    def add_lane(self, lane, orientation: Orientation):
        """
        If necessary, expand grid to include Lane at the designated row or column number
        The model defines a Lane as "either a Row or Column"
        :param lane:
        :param orientation:
        """
        # Add enough columns or rows for the desired Lane
        # TODO: Refactor grid to at least include addrows addcols methods
        if orientation == Orientation.Horizontal:
            rows_to_add = max(0, lane - len(self.Row_boundaries[1:]))
            for r in range(rows_to_add):
                self.add_row(connector_layout.Default_new_path_row_height)
        else:
            columns_to_add = max(0, lane - len(self.Col_boundaries[1:]))
            for c in range(columns_to_add):
                self.add_column(connector_layout.Default_new_path_col_width)

    def place_single_cell_node(self, node: SingleCellNode):
        """Places the node adding any required rows or columns"""

        # Determine whether or not we'll need to extend upward or rightward
        rows_to_add = max(0, node.Row - len(self.Row_boundaries[1:]))
        columns_to_add = max(0, node.Column - len(self.Col_boundaries[1:]))

        # If there is already a node at that location, raise an exception
        if not rows_to_add and not columns_to_add and self.Cells[node.Row - 1][node.Column - 1]:
            self.logger.error(f'Cell overlap at [{node.Row}, {node.Column}]')
            raise CellOccupiedFE

        # Add necessary rows and columns, if any
        horizontal_padding = self.Cell_padding.left + self.Cell_padding.right
        vertical_padding = self.Cell_padding.top + self.Cell_padding.bottom
        new_cell_height = node.Size.height + vertical_padding
        new_cell_width = node.Size.width + horizontal_padding
        default_cell_height = node.Node_type.Default_size.height
        default_cell_width = node.Node_type.Default_size.width

        # Check for horizontal overlap
        if not columns_to_add:
            overlap = max(0, node.Size.width + horizontal_padding - span(self.Col_boundaries, node.Column, node.Column))
            if overlap:
                # add the overlap to each col width from the right boundary rightward
                self.Col_boundaries = expand_boundaries(
                    boundaries=self.Col_boundaries, start_boundary=node.Column, expansion=overlap)
                # Check to see if the rightmost column position is now outside the diagram area
                if self.Col_boundaries[-1] > self.Diagram.Size.width:
                    raise SheetWidthExceededFE

        # Check for vertical overlap
        if not rows_to_add:
            overlap = max(0, node.Size.height + vertical_padding - span(self.Row_boundaries, node.Row, node.Row))
            if overlap:
                # add the overlap to each row ceiling from the top of this cell upward
                self.Row_boundaries = expand_boundaries(
                    boundaries=self.Row_boundaries, start_boundary=node.Row, expansion=overlap)
                # Check to see if the rightmost column position is now outside the diagram area
                if self.Row_boundaries[-1] > self.Diagram.Size.height:
                    raise SheetHeightExceededFE

        # Add extra rows and columns (must add the rows first)
        for r in range(rows_to_add):
            # Each new row, except the last will be of default height with the last matching the required height
            add_height = new_cell_height if r == rows_to_add - 1 else default_cell_height
            self.add_row(add_height)
        for c in range(columns_to_add):
            add_width = new_cell_width if c == columns_to_add - 1 else default_cell_width
            self.add_column(add_width)

        # Place the node in the new location
        self.Cells[node.Row - 1][node.Column - 1] = node
        self.Nodes.append(node)
