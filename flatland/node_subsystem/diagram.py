"""
diagram.py
"""
from flatland.node_subsystem.diagram_type import DiagramType
from flatland.flatland_exceptions import NotationUnsupportedForDiagramType, UnsupportedDiagramType
from flatland.datatypes.geometry_types import Position, Padding, Rect_Size
from flatland.node_subsystem.grid import Grid
from typing import TYPE_CHECKING
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_

if TYPE_CHECKING:
    from flatland.node_subsystem.canvas import Canvas


class Diagram:
    """
    The Diagram covers a rectangle within the area inside the Canvas margin.  Use padding to specify
    the extent and location of the diagram.  An origin and rectangle size will be derived from that
    for internal usage.

        Attributes

        - Canvas (obj) -- Drawn on this Canvas
        - Diagram_type (str) -- Type of model diagram to be drawn, class, for example
        - Notation (str) -- The supported notation used on this diagram
        - Grid (obj) -- All content in the diagram is organized within the cells of this Grid
        - Padding (Padding) -- Space between Canvas margin and Diagram on all sides (useful for specification)
        - Origin (Position) -- Lower left corner of Diagram in Canvas coordinates
        - Size (Rect_Size) -- Size of the Diagram rectangle within the Canvas

    """

    def __init__(self, canvas: 'Canvas', diagram_type_name: str, presentation: str, notation_name: str):
        """
        Constructor

        :param canvas: Reference to the Canvas
        :param diagram_type_name: A supported type of model diagram such as class, state machine, collaboration
        :param presentation: A predefined set of style specifications such as default, diagnostic, fullcolor
        :param notation_name: A supported notation such as xUML, Starr, Shlaer-Mellor
        """
        self.Canvas = canvas
        self.Presentation = presentation

        # Validate notation for this diagram type
        dnots = fdb.MetaData.tables['Diagram Notation']
        q = select([dnots]).where(
            and_(dnots.c['Notation'] == notation_name,
                 dnots.c['Diagram type'] == diagram_type_name)
        )
        i = fdb.Connection.execute(q).fetchone()
        if not i:
            raise NotationUnsupportedForDiagramType
        self.Notation = notation_name

        # Validate diagram type name
        dtypes = fdb.MetaData.tables['Diagram Type']
        q = dtypes.select(dtypes.c['Name'] == diagram_type_name)
        i = fdb.Connection.execute(q).fetchone()
        if not i:
            raise UnsupportedDiagramType
        # self.Diagram_type = diagram_type_name
        # Testing this now to replace above line
        self.Diagram_type = DiagramType(name=diagram_type_name, notation=self.Notation)
        self.Grid = Grid(diagram=self)  # Start with an empty grid
        self.Padding = Padding(top=0, bottom=0, left=0, right=0)
        self.Origin = Position(
            x=self.Canvas.Margin.left + self.Padding.left,
            y=self.Canvas.Margin.bottom + self.Padding.bottom
        )
        self.Size = Rect_Size(  # extent from origin to right or upper canvas margin
            width=self.Canvas.Size.width - self.Origin.x - self.Canvas.Margin.right,
            height=self.Canvas.Size.height - self.Origin.y - self.Canvas.Margin.top
        )

    def render(self):
        self.Grid.render()

    def __repr__(self):
        return f'Diagram: {self.Diagram_type}, Notation: {self.Notation}, Grid: {self.Grid}, Padding: {self.Padding},' \
               f'Origin: {self.Origin}, Size: {self.Size}'
