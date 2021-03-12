"""
tablet.py – Flatland binds a Canvas instance in the Flatland Application domain to a Tablet instance
in the drawing domain. The Tablet can be drawn using cairo or some other graphics drawing framework.
"""
import logging
from flatland.flatland_exceptions import NonSystemInitialLayer
from flatland.datatypes.geometry_types import Rect_Size, Position
import cairo
from flatland.drawing_domain.styledb import StyleDB
from flatland.drawing_domain.layer import Layer
from typing import Optional


class Tablet:
    """
    The Tablet class is part of the drawing_domain which provides a service to the Flatland model
    diagram application. We can imagine a virtual Tablet that the application uses to draw
    all of its nodes and connectors and other model elements. The Tablet abstracts away the details
    of drawing and graphics library interaction from the fundamental Flatland application.

    For example, when a Flatland node compartment wants to draw itself, it doesn't worry about line
    widths, dash patterns and colors. It also doesn't worry about flipping to whatever coordinate
    system the graphics library uses. A compartment would just say "add_shape( asset, size, location )" and
    the Tablet will take care of the rest. Here the asset is the name of the model entity 'compartment',
    the size in points (or whatever units the Flatland app wants to use) and location expressed in Flatland
    Canvas coordinates.

    When a blank Flatland Canvas is created, it will initialize its underlying Tablet and select a predefined
    drawing Type ('class diagram', 'state machine diagram' etc.) and Presentation Style ('default', 'formal',
    'diagnostic', etc).  The Diagram Type determines what kinds of things might be drawn, Assets such as 'connector',
    'compartment', 'class name', etc., while the Presentation Style establishes the Text and Line Styles to
    be used when drawing those Assets. All of this information is stored in a database which the Tablet
    loads upon creation.

    Each time the application wants something drawn, it will ask Tablet to add the appropriate Asset
    to one of its draw lists. A separate list is maintained for all the rectangles, line segments and
    text lines to be rendered. When the application is finished populating these lists, the Tablet can
    render everything using its graphic library, such as Cairo, using whatever coordinate system the
    library supplies, making any necessary conversions from the application coordinate system.

    Consequently, a new graphics library, such as NumPy for example, can be supported by updating the drawing_domain
    and primarily the Tablet class without having to make any changes in the Flatland application. Futhermore, any
    changes to text styles, colors, line patterns etc can be perfomred by updating the drawing_domain's style
    database.

        Attributes

        - Size -- The size of the whatever surface (PDF, RGB, SVG, etc) Tablet supports.
        - Output_file -- A filename or output stream object to be output as a drawing
        - PDF_sheet -- For now we only support PDF output as defined in Cairo.  So this is a Cairo surface
        - Context -- A Cairo context object for drawing on the PDF sheet
    """

    def __init__(self, size: Rect_Size, output_file, drawing_type: str, presentation: str, layer: str):
        """
        Constructs a new Tablet instance
        :param size: Vertical and horizontal span of the entire draw surface in points
        :param output_file: Name of the drawing file to be generated, PDF only for now
        :param drawing_type: Type of drawing so we can determine what kinds text and graphics can be drawn
        :param presentation: The layer's Presentation to load
        :param layer: The initial layer to be created on this Tablet (usually 'diagram')
        """
        self.logger = logging.getLogger(__name__)

        # Load all of the common font, color, etc. styles used by all Presentations from the
        # Flatland DB
        StyleDB()

        # Establish a system default layer ordering. Not all of them will be used in any given
        # Drawing, but this is the draw order from bottom-most layer upward
        # It can (should be) customizable by the user, but this should work for most diagrams
        self.layer_order = ['sheet', 'grid', 'frame', 'diagram', 'scenario', 'annotation']
        self.Presentations = {}  # Presentations loaded from the Flatland database, updated by Layer class

        if layer not in self.layer_order:
            raise NonSystemInitialLayer
        self.layers = {layer: Layer(name=layer, tablet=self, presentation=presentation, drawing_type=drawing_type)}
        # Initialize the first layer at the indicated position. If the position is not in the system layer order
        # list, it will be placed as the topmost layer. Usually, though, the initial layer should be diagram

        self.Drawing_type = drawing_type  # class diagram, state diagram, etc
        self.Size = size
        self.Output_file = output_file
        self.PDF_sheet = cairo.PDFSurface(self.Output_file, self.Size.width, self.Size.height)
        self.Context = cairo.Context(self.PDF_sheet)

    def add_layer(self, name: str, presentation: str, drawing_type: str) -> Optional[Layer]:
        """Add a new layer if not already instantiated and return it"""
        if not self.layers.get(name):
            self.layer_order.append(name)
            self.layers[name] = Layer(name=name, tablet=self, presentation=presentation, drawing_type=drawing_type)
            return self.layers[name]
        else:
            self.logger.warning(f"Layer: [{name}] previously instantiated")
            return None

    def render(self):
        """
        Renders each instantiated layer of the Tablet moving up the z axis. Any uninstantiated layers are skipped.
        """
        [self.layers[name].render() for name in self.layer_order if self.layers.get(name)]

    def to_dc(self, tablet_coord: Position) -> Position:
        """
        To display coordinates – Convert tablet bottom_left origin coordinate to
        display coordinate where top-left origin is used.
        """
        assert tablet_coord.y <= self.Size.height, "Tablet bounds exceeded"
        assert tablet_coord.x >= 0, "Negative x value"
        assert tablet_coord.y >= 0, "Negative y value"
        return Position(x=tablet_coord.x, y=self.Size.height - tablet_coord.y)

    def __repr__(self):
        return f'Size: {self.Size}, Dtype: {self.Drawing_type},' \
               f'Output: {self.Output_file}'
