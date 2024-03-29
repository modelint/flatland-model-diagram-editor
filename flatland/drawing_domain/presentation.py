"""
presentation.py – Presentation class in Drawing domain
"""
import logging
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_
from collections import namedtuple

CornerSpec = namedtuple('Corner_Spec', 'radius top bottom')

class Presentation:
    """
   A set of compatible visual styles including fonts, colors, border widths and so forth as appropriate to a
   given Drawing Type form a selectable Presentation. For example, an `Executable UML State Machine Diagram`
   might be drawn using certain fonts for state names and possibly different colors for transient and
   non-transient states. Alternatively, only black and white might be used with purple for a certain kind of
   connector in a diagnostic Presentation.
   """

    def __init__(self, name: str, drawing_type: str):
        """
       Constructor
       """
        self.logger = logging.getLogger(__name__)
        self.Name = name
        self.Drawing_type = drawing_type
        self.Text_presentation = {}
        self.Underlays = set()  # Set of text presentations that require an underlay
        self.Shape_presentation = {}
        self.Closed_shape_fill = {}
        self.Corner_spec = {}

        # Load Asset Presentations for all Assets in this Presentation
        self.logger.info(f"Loading assets for Presentation [{self.Name}]")
        self.load_text_presentations()
        self.load_shape_presentations()

    def load_text_presentations(self):
        """
        For each text Asset in this Presentation, load its Text Presentation
        """
        text_pres_t = fdb.MetaData.tables['Text Presentation']
        p = [text_pres_t.c.Asset, text_pres_t.c['Text style'], text_pres_t.c.Underlay]
        s = and_(text_pres_t.c.Presentation == self.Name, text_pres_t.c['Drawing type'] == self.Drawing_type)
        q = select(p).where(s)
        f = fdb.Connection.execute(q).fetchall()
        for i in f:
            self.Text_presentation[i.Asset] = i['Text style']
            if i['Underlay']:
                self.Underlays.add(i.Asset)

    def load_shape_presentations(self):
        """
        For each shape Asset in this Presentation, load its Shape Presentation
        """
        shape_pres_t = fdb.MetaData.tables['Shape Presentation']
        q = select([shape_pres_t.c.Asset, shape_pres_t.c['Line style']]).where(and_(
            shape_pres_t.c.Presentation == self.Name, shape_pres_t.c['Drawing type'] == self.Drawing_type
        ))
        f = fdb.Connection.execute(q).fetchall()
        for i in f:
            self.Shape_presentation[i.Asset] = i['Line style']

        shape_fill_t = fdb.MetaData.tables['Closed Shape Fill']
        q = select([shape_fill_t.c.Asset, shape_fill_t.c.Fill]).where(and_(
            shape_fill_t.c.Presentation == self.Name, shape_fill_t.c['Drawing type'] == self.Drawing_type
        ))
        f = fdb.Connection.execute(q).fetchall()
        for i in f:
            self.Closed_shape_fill[i.Asset] = i.Fill

        corner_spec_t = fdb.MetaData.tables['Corner Spec']
        p = [corner_spec_t.c.Asset, corner_spec_t.c.Radius, corner_spec_t.c.Top, corner_spec_t.c.Bottom]
        q = select(p).where(and_(
            corner_spec_t.c.Presentation == self.Name, corner_spec_t.c['Drawing type'] == self.Drawing_type
        ))
        f = fdb.Connection.execute(q).fetchall()
        for i in f:
            self.Corner_spec[i.Asset] = CornerSpec(radius=i.Radius, top=i.Top, bottom=i.Bottom)