"""
layout_specification.py – These are the default values used for layout
"""

from flatland.datatypes.geometry_types import Padding, Position, Alignment, VertAlign, HorizAlign

# Layout Specification
# The distance from each canvas edge that may not be occupied by the Diagram
default_margin = Padding(top=10, bottom=10, left=10, right=10)

# The lower left corner of the Diagram in Canvas coordinates
default_diagram_origin = Position(x=0, y=0)  # Relative to the Canvas margin

# The distance from each Cell edge inward that may not be occupied by any Node. This prevents two Nodes in
# adjacent Cells from being too close together.
default_cell_padding = Padding(top=5, bottom=5, left=5, right=5)

# The horizontal and vertical alignment of a Node within its Cell(s)
default_cell_alignment = Alignment(vertical=VertAlign.CENTER, horizontal=HorizAlign.CENTER)


# Connector Layout Specification

# The number of equally spaced positions relative to a center position (included in the count) on a Node face where
# a Stem can be attached. A value of one corresponds to a single connection point in the center of a Node face.
# A value of three is a central connection point with one on either side, and so on. In practice, five is usually the
# right number, especially for a class or state diagram.  But this could vary by diagram and node type in the future.
default_stem_positions = 5

# The number of ruts where Path can be defined in a Lane
# These work like stem/anchor positions on a Lane as opposed to a Node face
# For a value of 3 we get positions -1, 0 and +1 with 0 representing the Lane Center
# and +1 high/right and -1 low/left
default_rut_positions = 5

# For a Stem that has no graphic decoration, such as an xUML class binary association connection or a xUML subclass
# connection, this is the minimum distance from the node face to either a bend or the opposing Stem end. It prevents
# a bend too close to a Node face or a connection too close to another Node.
undecorated_stem_clearance = 11

# When adding an empty row or column to acommodate a Path in a Connector use these
default_new_path_row_height = 100
default_new_path_col_width = 100

# The distance from the root end on the Node face to the vine end just before any vine end
# shape decorations are drawn
default_unary_branch_length = 48
