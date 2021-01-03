"""
diagram_layout_specification.py
"""

from flatland.database.flatlanddb import FlatlandDB as fdb
from flatland.datatypes.geometry_types import Padding, Position, Alignment, HorizAlign, VertAlign
from sqlalchemy import select

# To convert db string values to our alignment enums
# We can't just use enum values themselves since int values are used by linear geometry, so we need this addtional map
halign_map = {"left": HorizAlign.LEFT, "center": HorizAlign.CENTER, "right": HorizAlign.RIGHT}
valign_map = {"top": VertAlign.TOP, "center": VertAlign.CENTER, "bottom": VertAlign.BOTTOM}


class DiagramLayoutSpecification:
    """
    Diagram Layout Specification

    Defines a set of values that determine how a Diagram and Grid is positioned on a Canvas and
    how Nodes are positioned relative to the Diagram and Grid.

        Attributes

        - Default margin -- The Canvas area surrounding the Diagram, can be zero
        - Default diagram origin -- The default lower left corner of the Diagram in Canvas coordinates
        - Default cell padding -- The minimum cell area surrounding a Node, can be zero, but shouldn't be since it
          prevents nodes in adjacent cells from touching
        - Default cell alignment -- Default alignment of Node within its Cell, typically center, center
    """
    Default_margin = None
    Default_diagram_origin = None
    Default_cell_padding = None
    Default_cell_alignment = None

    def __init__(self):
        """
        Constructor - Load values from database
        """
        spec = fdb.MetaData.tables['Diagram Layout Specification']
        q = select([spec])
        i = fdb.Connection.execute(q).fetchone()
        assert i, "No Diagram Layout Specification in database"

        DiagramLayoutSpecification.Default_margin = Padding(
            top=i['Default margin top'], bottom=i['Default margin bottom'],
            left=i['Default margin left'], right=i['Default margin right']
        )

        DiagramLayoutSpecification.Default_diagram_origin = Position(
            x=i['Default diagram origin x'], y=i['Default diagram origin y']
        )

        DiagramLayoutSpecification.Default_cell_padding = Padding(
            top=i['Default cell padding top'], bottom=i['Default cell padding bottom'],
            left=i['Default cell padding left'], right=i['Default cell padding right']
        )

        DiagramLayoutSpecification.Default_cell_alignment = Alignment(
            vertical=halign_map[i['Default cell alignment vertical']],
            horizontal=valign_map[i['Default cell alignment horizontal']]
        )
