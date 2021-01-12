"""
styledb.py
"""
import logging
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_
from collections import namedtuple


Float_RGB = namedtuple('Float_RGB', 'R G B')
Line_Style = namedtuple('Line_Style', 'pattern width color')
Text_Style = namedtuple('Text_Style', 'typeface size slant weight color spacing')
Dash_Pattern = namedtuple('Dash_Pattern', 'solid blank')


class StyleDB:
    rgbF = {}  # rgb color float representation
    dash_pattern = {}
    line_style = {}
    typeface = {}
    text_style = {}
    fill_style = {}
    shape_presentation = {} # asset : style (for loaded presentation)
    text_presentation = {}

    def __init__(self, drawing_type, presentation):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Loading styles from flatland db")
        load_colors()
        load_dash_patterns()
        load_line_styles()
        load_typefaces()
        load_text_styles()
        load_asset_presentations(drawing_type=drawing_type, presentation=presentation)
        self.logger.info("presentations loaded from flatland db")

# TODO: change to static methods
def load_colors():
    colors = fdb.MetaData.tables['Color']
    q = select([colors])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.rgbF[i.Name] = Float_RGB(R=round(i.R / 255, 2), G=round(i.G / 255, 2), B=round(i.B / 255, 2))


def load_dash_patterns():
    patterns = fdb.MetaData.tables['Dash Pattern']
    q = select([patterns])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        if not i.Solid and not i.Blank:
            StyleDB.dash_pattern[i.Name] = []
        else:
            StyleDB.dash_pattern[i.Name] = Dash_Pattern( solid=i.Solid, blank=i.Blank )

def load_typefaces():
    tface_t = fdb.MetaData.tables['Typeface']
    q = select([tface_t])
    rows = fdb.Connection.execute(q).fetchall()
    for r in rows:
        StyleDB.typeface[r.Alias] = r.Name

def load_text_styles():
    tstyle = fdb.MetaData.tables['Text Style']
    q = select([tstyle])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.text_style[i.Name] = Text_Style(
            typeface=StyleDB.typeface[i.Typeface], size=i.Size, slant=i.Slant, weight=i.Weight, color=i.Color, spacing=i.Spacing)


def load_line_styles():
    lstyles = fdb.MetaData.tables['Line Style']
    q = select([lstyles])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.line_style[i.Name] = Line_Style( pattern=i.Pattern, width=i.Width, color=i.Color )


def load_asset_presentations(presentation: str, drawing_type: str):
    shape_pres_t = fdb.MetaData.tables['Shape Presentation']
    q = select([shape_pres_t.c.Asset, shape_pres_t.c['Line style']]).where( and_(
        shape_pres_t.c.Presentation == presentation, shape_pres_t.c['Drawing type'] == drawing_type
    ))
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.shape_presentation[i.Asset] = i['Line style']

    shape_fill_t = fdb.MetaData.tables['Closed Shape Fill']
    q = select([shape_fill_t.c.Asset, shape_fill_t.c.Fill]).where( and_(
        shape_fill_t.c.Presentation == presentation, shape_fill_t.c['Drawing type'] == drawing_type
    ))
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.fill_style[i.Asset] = i.Fill

    text_pres_t = fdb.MetaData.tables['Text Presentation']
    q = select([text_pres_t.c.Asset, text_pres_t.c['Text style']]).where( and_(
        text_pres_t.c.Presentation == presentation, text_pres_t.c['Drawing type'] == drawing_type
    ))
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.text_presentation[i.Asset] = i['Text style']
