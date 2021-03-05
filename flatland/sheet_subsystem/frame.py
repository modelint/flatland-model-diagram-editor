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
        self.Databox = {}
        self.Box_fields = []

        # The Frame's drawing type name is composed from the frame's name and size
        drawing_type_name = ' '.join([name, self.Canvas.Sheet.Size_group])  # e.g. "OS Engineer large"
        # Now create a Layer for the Frame
        self.Layer = self.Canvas.Tablet.add_layer(
            name='frame', presentation=presentation, drawing_type=drawing_type_name
        )  # Now we have a surface to draw the frame on!

        # If there is a title block placement specified for this Frame, get the name of the pattern
        tb_placement_t = fdb.MetaData.tables['Title Block Placement']
        f = and_(
            (tb_placement_t.c['Frame'] == self.Name),
            (tb_placement_t.c['Sheet'] == self.Canvas.Sheet.Name),
        )
        query = select([tb_placement_t.c['Title block pattern']]).select_from(tb_placement_t).where(f)
        row = fdb.Connection.execute(query).fetchone()
        self.Title_block_pattern = None if not row else row[0]

        if self.Title_block_pattern:
            # Build a text block for each Data Box containing the Metadata Text Content
            # Resource Metacontent (graphics) is not allowed like it is for Open Fields, so
            # we assume all Metacontent is text
            boxline_t = fdb.MetaData.tables['Box Text Line']
            p = [boxline_t.c.Box, boxline_t.c.Order, boxline_t.c.Metadata]
            q = select(p).where(boxline_t.c['Title block pattern'] == self.Title_block_pattern).order_by(
                boxline_t.c.Box, boxline_t.c.Order)
            rows = fdb.Connection.execute(q).fetchall()
            # Lookup the Text Content for each Box Text Line and create
            # a text block for each Data Box
            for r in rows:
                if r.Box in self.Databox:
                    # The Data Box was recorded with an initial text line, so this must be an additional line
                    self.Databox[r.Box].append(metadata[r.Metadata][0])
                else:
                    # Rows are ordered by Data Box, so if the box id is new, we create an initial dictioary entry
                    # With level 1
                    self.Databox[r.Box] = [metadata[r.Metadata][0]]

            # TODO: Join Data Box/Box/Box Placement to get Placement
            # TODO: and Data Box alignment
            # TODO: Put all this in the Databox record

            # Get the margin to use in each Data Box
            tb_place_t = fdb.MetaData.tables['Title Block Placement']
            scaledtb_t = fdb.MetaData.tables['Scaled Title Block']
            p = [scaledtb_t.c['Margin H'], scaledtb_t.c['Margin V']]
            j = tb_place_t.join(scaledtb_t)
            q = select(p).select_from(j).where(tb_place_t.c.Frame == self.Name)
            row = fdb.Connection.execute(q).fetchone()
            assert row, f"No Title Block Placement for frame: {name}"
            h_margin, v_margin = row
            # text_box_corner = Position()
            print()






        # Render the non-title block fields
        open_field_t = fdb.MetaData.tables['Open Field']

        f = and_(
            (open_field_t.c['Frame'] == self.Name),
            (open_field_t.c['Sheet'] == self.Canvas.Sheet.Name)
        )
        q = select([open_field_t]).where(f)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            p = Position(r['x position']*points_in_mm, r['y position']*points_in_mm)
            ma = Rect_Size(r['max height']*points_in_mm, r['max width']*points_in_mm)
            self.Open_fields.append(
                FieldPlacement(metadata=r.Metadata, position=p, max_area=ma)
            )
        self.render()


        # Now render the title block fields

        print()

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

        # Fill in each box field


