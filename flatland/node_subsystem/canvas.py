"""
canvas.py

This is the Flatland (and not the cairo) Canvas class
"""
import sys
import logging
from flatland.flatland_exceptions import InvalidOrientation, NonSystemInitialLayer
from flatland.node_subsystem.diagram_layout_specification import DiagramLayoutSpecification
from flatland.connector_subsystem.connector_layout_specification import ConnectorLayoutSpecification
from flatland.datatypes.geometry_types import Rect_Size, Padding
from flatland.node_subsystem.diagram import Diagram
from flatland.drawing_domain.tablet import Tablet
from flatland.sheet_subsystem.sheet import Sheet, Group
from flatland.decoration_subsystem.symbol import Symbol

# All sheet and canvas related constants are kept together here for easy review and editing
points_in_cm = 28.3465
points_in_mm = 2.83465
points_in_inch = 72


class Canvas:
    """
    You can think of a Canvas as a sheet of paper, typically, not necessarily of a standard size
    such as A1, Tabloid or 8.5 x 11. It represents the total space where any drawing may occur.
    Typically, though, a margin is specified to preserve empty space along the edges of the Canvas.
    The margin can be set to zero all the way around if desired.

        Attributes

        - Sheet (str) -- A standard name such as letter and tabloid in the US or A2 in Europe to describe sheet size
        - Orientation (str) -- *portrait* or *landscape*
        - Size (Rect_Size) -- The size in points as a Rect_Size named tuple
        - Margin (Padding) -- The default amount of space surrounding a Node in a Cell
        - Diagram (obj) -- Instance of Diagram drawn on this Canvas
        - Tablet (obj) -- This is a proxy for the underlying graphics drawing context
        - Show_margin (boolean) -- Draw the margin? For diagnostic purposes only

    """

    def __init__(self, diagram_type: str, presentation: str, notation: str, standard_sheet_name: str, orientation: str,
                 diagram_padding: Padding, show_grid: bool, drawoutput=sys.stdout.buffer):
        """
        Constructor

        :param diagram_type: A supported type of model diagram such as class, state machine, collaboration
        :param presentation: A predefined set of style specifications such as default, diagnostic, fullcolor
        :param notation: A supported notation such as xUML, Starr, Shlaer-Mellor
        :param standard_sheet_name: A US or international printer sheet size such as A1, tabloid, letter
        :param orientation: portrait or landscape
        :param drawoutput: A standard IO binary object obtained from sys
        """
        self.logger = logging.getLogger(__name__)
        # Load layout specifications
        DiagramLayoutSpecification()
        ConnectorLayoutSpecification()

        self.Sheet = Sheet(standard_sheet_name)  # Ensure that the user has specified a known sheet size
        if orientation not in ('portrait', 'landscape'):
            raise InvalidOrientation(orientation)
        self.Orientation = orientation
        # We want to convert all units, inch, mm, etc to points since that's all we use from here on
        factor = points_in_inch if self.Sheet.Group == Group.US else points_in_cm

        # Set point size height and width based on portrait vs. landscape orientation
        h, w = (self.Sheet.Size.height, self.Sheet.Size.width) if self.Orientation == 'landscape' else (
            self.Sheet.Size.width, self.Sheet.Size.height)
        self.Size = Rect_Size(
            height=int(round(h * factor)),
            width=int(round(w * factor))
        )
        self.Margin = DiagramLayoutSpecification.Default_margin

        # Create the one and only Tablet instance and initialize it with the Presentation on the diagram
        # Layer
        try:
            self.Tablet = Tablet(
                size=self.Size, output_file=drawoutput,
                # Drawing types include notation such as 'xUML class diagram' since notation affects the choice
                # of shape and text styles.  An xUML class diagram association class stem is dashed, for example.
                drawing_type=' '.join([notation, diagram_type, 'diagram']), presentation=presentation,
                layer='diagram'
            )
        except NonSystemInitialLayer:
            self.logger.exception("Initial layer [diagram] not found in Tablet layer order")
            sys.exit()
        self.Diagram = Diagram(
            self, diagram_type_name=diagram_type, layer=self.Tablet.layers['diagram'],
            notation_name=notation, padding=diagram_padding, show_grid=show_grid
        )
        # Load symbol data
        self.logger.info("Loading symbol decoration data from flatland database")
        Symbol(diagram_type=self.Diagram.Diagram_type.Name, notation=self.Diagram.Notation)

    def render(self):
        """
        Draw all content of this Canvas onto the Tablet
        """
        # Now add all Diagram content to the Tablet
        self.Diagram.render()

        # Draw all added content and output a PDF using whatever graphics library is configured in the Tablet
        self.Tablet.render()

    def __repr__(self):
        return f'Canvas(diagram_type={self.Diagram.Diagram_type}, layer={self.Diagram.Layer},' \
               f'notation={self.Diagram.Notation}, standard_sheet_name={self.Sheet}, orientation={self.Orientation},' \
               f'drawoutput={self.Tablet.Output_file} )'

    def __str__(self):
        return f'Sheet: {self.Sheet}, Orientation: {self.Orientation}, '\
               f'Canvas size: h{self.Size.height} pt x w{self.Size.width} pt Margin: {self.Margin}'
