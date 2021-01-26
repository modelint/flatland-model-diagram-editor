"""frame.py – Draws the selected frame sized to a given sheet and fills in the fields"""

from sqlalchemy import select, and_
from flatland.database.flatlanddb import FlatlandDB as fdb
from flatland.datatypes.geometry_types import Position, Rect_Size
from flatland.node_subsystem.canvas import points_in_cm
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from flatland.node_subsystem.canvas import Canvas

points_in_mm = 2.83465

class Frame:
    """
    On any serious project it is not adequate to generate model diagrams absent any meta data such as
    authors, dates, revision numbers, copyright notices, organization logos and so forth.
    A Frame represents a pattern of Fields and/or a Title Block Pattern on the surface area defined by
    a Sheet. The lower left corner placements of each Frame element (Field or Scaled Title Block) are
    customized to fit the dimensions of a given Sheet.
    """

    def __init__(self, name: str, canvas: 'Canvas', metadata: Dict[str, str]):
        """
        Constructor
        """
        self.Name = name
        self.Canvas = canvas
        self.metadata = metadata
        self.Open_fields = {}

        open_field_t = fdb.MetaData.tables['Open Field']

        f = and_(
            (open_field_t.c['Frame'] == self.Name),
            (open_field_t.c['Sheet'] == self.Canvas.Sheet.Name)
        )
        query = select([open_field_t]).where(f)
        rows = fdb.Connection.execute(query).fetchall()
        for r in rows:
            content = r.Metadata
            # If missing content, log warning
            of_dataloc = ':'.join([r.Metadata, r.Location])
            p = Position(r['x position']*points_in_mm, r['y position']*points_in_mm)
            a = Rect_Size(r['max height']*points_in_mm, r['max width']*points_in_mm)
            print()

