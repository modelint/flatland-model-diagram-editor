"""
titleblock_placement.py -  Title Block Placement class modeled in the Sheet Subsystem
"""
from sqlalchemy import select, and_
from collections import namedtuple
from flatland.database.flatlanddb import FlatlandDB as fdb
from flatland.datatypes.geometry_types import Position, Rect_Size
from flatland.node_subsystem.canvas import points_in_mm
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.drawing_domain.layer import Layer
    from flatland.sheet_subsystem.sheet import Sheet

CompartmentBox = namedtuple("_CompartmentBox", "distance upper_box lower_box")
BoxPlacement = namedtuple("_BoxPlacement", "placement size")


def draw_titleblock(frame: str, sheet: 'Sheet', layer: 'Layer'):
    """
    Draw each box in the title block on the specified layer

    :param layer:  Layer to draw the box on
    :param frame:  Title block is fitted to this frame
    :param sheet:  Frame is drawn on this Sheet (sizing info)
    :return:
    """
    bplace_t = fdb.MetaData.tables['Box Placement']

    p = [bplace_t.c.X, bplace_t.c.Y, bplace_t.c.Height, bplace_t.c.Width]
    f = and_(
        (bplace_t.c.Frame == frame),
        (bplace_t.c.Sheet == sheet.Name)
    )
    q = select(p).select_from(bplace_t).where(f)
    rows = fdb.Connection.execute(q).fetchall()
    for r in rows:
        layer.add_rectangle(
            asset='Block border', lower_left=Position(r.X, r.Y),
            size=Rect_Size(height=r.Height, width=r.Width)
        )


def compute_box_placements(pattern: str, placement: Position, size: Rect_Size) -> Dict[int, BoxPlacement]:
    """
    Computes the lower left corner and size of every box in a Title Block Placement

    :param pattern: The Title Block Pattern to be computed
    :param placement:  The lower left corner for its Frame in Canvas Coordinates
    :param size:  The size of the Envelope enclosing the entire pattern
    :return: A dictionary of Box Placements indexed by Box ID
    """
    # Create the Box Placement for the Envelope Box (always ID:1)
    boxplacements = {1: BoxPlacement(size=size, placement=placement)}

    # Process each remaining Section (Compartment) Box Partition until we are left with nothing but Data Boxes
    compbox_t = fdb.MetaData.tables['Compartment Box']
    q = compbox_t.select().where(compbox_t.c.Pattern == pattern).order_by(compbox_t.c.ID)
    rows = fdb.Connection.execute(q).fetchall()
    for p in rows:  # For each Partition
        enclosing_box = boxplacements[p.ID]
        if p.Orientation == 'H':  # Horizontal partition splitting the Y axis
            x_down = enclosing_box.placement.x
            y_down = enclosing_box.placement.y
            w_down = enclosing_box.size.width
            h_down = round((p.Distance * enclosing_box.size.height), 2)
            boxplacements[p.Down] = BoxPlacement(
                size=Rect_Size(width=w_down, height=h_down), placement=Position(x_down, y_down)
            )
            x_up = x_down
            w_up = w_down
            y_up = round(y_down + h_down, 2)
            h_up = round((enclosing_box.size.height - h_down), 2)
            boxplacements[p.Up] = BoxPlacement(
                size=Rect_Size(width=w_up, height=h_up), placement=Position(x_up, y_up)
            )
        else:  # Vertical partition splitting the X axis
            x_down = enclosing_box.placement.x
            y_down = enclosing_box.placement.y
            w_down = round((p.Distance * enclosing_box.size.width), 2)
            h_down = round(enclosing_box.size.height, 2)
            boxplacements[p.Down] = BoxPlacement(
                size=Rect_Size(width=w_down, height=h_down), placement=Position(x_down, y_down)
            )
            x_up = round(x_down + w_down, 2)
            w_up = round((enclosing_box.size.width - w_down), 2)
            y_up = y_down
            h_up = h_down
            boxplacements[p.Up] = BoxPlacement(
                size=Rect_Size(width=w_up, height=h_up), placement=Position(x_up, y_up)
            )
    return boxplacements


class TitleBlockPlacement:
    """
    Commputes the boundaries of a Scaled Title Block in a Frame and updates the flatland database
    This should be executed each time the flatland database is rebuilt
    """

    def __init__(self):

        self.population = []

        tb_place_t = fdb.MetaData.tables['Title Block Placement']
        scaledtb_t = fdb.MetaData.tables['Scaled Title Block']

        # We need each Title Block Placement combined with its Scaled Title Block.Block size
        # Join Title Block Placement and Scaled Title Block relvars and return the value (with unique attributes)
        p = [tb_place_t.c.Frame, tb_place_t.c.Sheet, tb_place_t.c['Title block pattern'],
             tb_place_t.c['Sheet size group'], tb_place_t.c.X, tb_place_t.c.Y, scaledtb_t.c.Width, scaledtb_t.c.Height]
        j = tb_place_t.join(scaledtb_t)
        q = select(p).select_from(j)
        rows = fdb.Connection.execute(q).fetchall()

        # Compute the box placements for each Title Block Placement
        for r in rows:
            boxplacements = compute_box_placements(
                pattern=r['Title block pattern'], placement=Position(
                    round(r.X*points_in_mm, 2), round(r.Y*points_in_mm, 2)),
                size=Rect_Size(width=round(r.Width*points_in_mm, 2), height=round(r.Height*points_in_mm, 2))
            )
            # Update flatland database with newly computed instances of Box Placement
            for k, v in boxplacements.items():
                d = {'Frame': r.Frame, 'Sheet': r.Sheet, 'Title block pattern': r['Title block pattern'],
                     'Box': k, 'X': v.placement.x, 'Y': v.placement.y, 'Height': v.size.height, 'Width': v.size.width}
                self.population.append(d)

        # Insert the population into the database
        bplace_t = fdb.MetaData.tables['Box Placement']
        fdb.Connection.execute(bplace_t.insert(), self.population)