"""
styledb.py - Loads styles from the flatland database common to all Presentations
"""
import logging
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select
from collections import namedtuple

Float_RGB = namedtuple('Float_RGB', 'R G B')
Line_Style = namedtuple('Line_Style', 'pattern width color')
Text_Style = namedtuple('Text_Style', 'typeface size slant weight color spacing')
Dash_Pattern = namedtuple('Dash_Pattern', 'solid blank')

def report_colors():
    colors = fdb.MetaData.tables['Color']
    p = [colors.c.Name]
    r = colors.c.Canvas  # This boolean value is true (Canvas ok)
    q = select(p).where(r)
    f = fdb.Connection.execute(q).fetchall()
    print("Canvas colors:")
    print("---")
    for i in f:
        print(i.Name)
    print("===")

def load_colors():
    colors = fdb.MetaData.tables['Color']
    q = select([colors])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.rgbF[i.Name] = Float_RGB(R=round(i.R / 255, 2), G=round(i.G / 255, 2), B=round(i.B / 255, 2))

def load_color_usages():
    usages = fdb.MetaData.tables['Color Usage']
    q = select([usages])
    f = fdb.Connection.execute(q).fetchall()
    for i in f:
        StyleDB.color_usage[i.Name] = i.Color

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


class StyleDB:
    """
    Singleton class interface to the Presentation and Styles in the Flatland database. Created with an initial
    Presentation and loads all presentation/style data for that Presentation for easy access by
    the Tablet.
    """
    rgbF = {}  # rgb color float representation
    dash_pattern = {}
    line_style = {}
    typeface = {}
    text_style = {}
    color_usage = {}

    def __init__(self, print_colors=False, rebuild=False):
        """
        Constructor

        :param print_colors: True if the user just wants a list of available canvas/usage colors
        :param rebuild: True if the user requests a database rebuild before reporting colors
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Loading common styles from Flatland db")
        # Load all common graphical and text styles in the database (regardless of what we might actually use)
        if print_colors:
            # The user wants a list of avaialable colors
            report_colors()
        else:
            load_colors()
            load_color_usages()
            load_dash_patterns()
            load_line_styles()
            load_typefaces()
            load_text_styles()