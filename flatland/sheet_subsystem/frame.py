"""frame.py – Draws the selected frame sized to a given sheet and fills in the fields"""

import logging
from sqlalchemy import select, and_
from flatland.database.flatlanddb import FlatlandDB as fdb
from collections import namedtuple
from flatland.datatypes.geometry_types import Position, Rect_Size
from flatland.node_subsystem.canvas import points_in_mm
from flatland.sheet_subsystem.resource import resource_locator
from flatland.sheet_subsystem.titleblock_placement import draw_titleblock
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from flatland.node_subsystem.canvas import Canvas


FieldPlacement = namedtuple('FieldPlacement', 'metadata position max_area')

class Frame:
    """
    On any serious project it is not adequate to generate model diagrams absent any meta data such as
    authors, dates, revision numbers, copyright notices, organization logos and so forth.
    A Frame represents a pattern of Fields and/or a Title Block Pattern on the surface area defined by
    a Sheet. The lower left corner placements of each Frame element (Field or Scaled Title Block) are
    customized to fit the dimensions of a given Sheet.
    """

    def __init__(self, name: str, presentation: str, canvas: 'Canvas', metadata: Dict[str, str]):
        """
        Constructor

        :param name:
        :param canvas:
        :param presentation:
        :param metadata:
        """
        self.logger = logging.getLogger(__name__)
        self.Name = name
        self.Canvas = canvas
        self.metadata = metadata
        self.Open_fields = []

        # The Frame's drawing type name is composed from the frame's name and size
        drawing_type_name = ' '.join([name, self.Canvas.Sheet.Size_group])  # e.g. "OS Engineer large"
        # Now create a Layer for the Frame
        self.Layer = self.Canvas.Tablet.add_layer(
            name='frame', presentation=presentation, drawing_type=drawing_type_name
        )

        # Now we have a surface to draw the frame on!

        # First render the non-title block fields
        open_field_t = fdb.MetaData.tables['Open Field']

        f = and_(
            (open_field_t.c['Frame'] == self.Name),
            (open_field_t.c['Sheet'] == self.Canvas.Sheet.Name)
        )
        query = select([open_field_t]).where(f)
        rows = fdb.Connection.execute(query).fetchall()
        for r in rows:
            p = Position(r['x position']*points_in_mm, r['y position']*points_in_mm)
            ma = Rect_Size(r['max height']*points_in_mm, r['max width']*points_in_mm)
            self.Open_fields.append(
                FieldPlacement(metadata=r.Metadata, position=p, max_area=ma)
            )
        self.render()

    def render(self):
        """Draw the Frame on its Layer"""
        self.logger.info('Rendering frame')

        # Fill each open field
        for f in self.Open_fields:
            a = ' '.join([f.metadata, 'open'])
            content, isresource = self.metadata.get(f.metadata, (None, None))
            # If there is no data supplied to fill in the field, just leave it blank and move on
            if content and isresource:
                # Content is a resource locator, get the path to the resource (image)
                rloc = resource_locator.get(content)
                if rloc:
                    self.Layer.add_image(resource_path=rloc, lower_left=f.position, size=f.max_area)
                else:
                    self.logger.warning(f"Couldn't find resource file for: [{content}]")
            elif content:  # Text content
                # Content is a line of text to print directly
                self.Layer.add_text_line(
                    asset=a,
                    lower_left=f.position,
                    text=content,
                )

        # Draw the title block, if any
        draw_titleblock(frame=self.Name, sheet=self.Canvas.Sheet.Name, layer=self.Layer)

        # TODO: Fill each box field (in a Title Block)

