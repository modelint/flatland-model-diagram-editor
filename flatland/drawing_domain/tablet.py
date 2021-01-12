"""
tablet.py – Flatland binds a Canvas instance in the Flatland Application domain to a Tablet instance
in the drawing domain. The Tablet can be drawn using cairo or some other graphics drawing framework.
"""
import logging
from flatland.datatypes.geometry_types import Rect_Size, Position, HorizAlign
from typing import List
import cairo
from flatland.drawing_domain.styledb import StyleDB
from collections import namedtuple

# These structures are intended for internal use only
# They each incoroporate style information with a more general geometric structure
# So that the Tablet can draw them in the correct presentation style
_Polygon = namedtuple('_Polygon', 'vertices border_style fill')
"""Closed polygon (other than a rectangle) that can be filled"""
_Line_Segment = namedtuple('_Line_Segment', 'from_here to_there style')
"""A line segment is drawn from one point on the Tablet to another using some line drawing style"""
_Rectangle = namedtuple('_Rectangle', 'upper_left size border_style fill')
"""A rectangle is positioned at its lower left corner and then drawn with the specified size"""
_Text_line = namedtuple('_Text_line', 'lower_left text style')
"""A line of text (no CR/LF characters) rendered with a given style"""

Cairo_font_weight = {'normal': cairo.FontWeight.NORMAL, 'bold': cairo.FontWeight.BOLD}
"""Maps an application style to a cairo specific font weight"""
Cairo_font_slant = {'normal': cairo.FontSlant.NORMAL, 'italic': cairo.FontSlant.ITALIC}
"""Maps an application style to a cairo specific font slant"""


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
        - Line_segments -- A list of geometric lines each with start and end coordinates.
        - Rectangles -- A list of rectangles each with a lower left corner, height and width
        - Polygons -- A list of closed polygons
        - Text -- A list of text lines (new lines are not supported)
        - Output_file -- A filename or output stream object to be output as a drawing
        - PDF_sheet -- For now we only support PDF output as defined in Cairo.  So this is a Cairo surface
        - Context -- A Cairo context object for drawing on the PDF sheet
    """

    def __init__(self, size: Rect_Size, output_file, drawing_type: str, presentation: str):
        """
        Constructs a new Tablet instance
        :param size: Vertical and horizontal span of the entire draw surface in points
        :param output_file: Name of the drawing file to be generated, PDF only for now
        :param drawing_type: Type of drawing so we can determine what kinds of shapes and text will be drawn
        :param presentation: User selected Presentation Style so we know which styles to load from the database
        """
        self.logger = logging.getLogger(__name__)

        # Load all of the draw styles from the flatland database
        # We only need to load the styles for the user selected Presentation Style and only for the Assets
        # that can be drawn in the given drawing Type
        StyleDB(drawing_type=drawing_type, presentation=presentation)

        self.Drawing_type = drawing_type  # class diagram, state diagram, etc
        self.Presentation = presentation  # informal, sexy, etc
        self.Size = size
        self.Line_segments: List[_Line_Segment] = []
        self.Polygons: List[_Polygon] = []
        self.Rectangles: List[_Rectangle] = []
        self.Text: List[_Text_line] = []
        self.Output_file = output_file
        self.PDF_sheet = cairo.PDFSurface(self.Output_file, self.Size.width, self.Size.height)
        self.Context = cairo.Context(self.PDF_sheet)

    def add_line_segment(self, asset: str, from_here: Position, to_there: Position):
        """
        Convert line segment coordinates to device coordinates and combine with the Line Style defined
        for the Asset in the selected Preentation Style
        :param asset:
        :param from_here:
        :param to_there:
        """
        self.Line_segments.append(_Line_Segment(
            from_here=self.to_dc(from_here), to_there=self.to_dc(to_there), style=StyleDB.shape_presentation[asset])
        )

    def add_open_polygon(self, asset: str, vertices: List[Position]):
        """
        Add all of the line segments necessary to draw the polygon to our list of line segments

        :param asset: Used to look up the line style
        :param vertices: A sequences of 2 or more vertices
        """
        for v1, v2 in zip(vertices, vertices[1:]):
            assert len(vertices) > 1, "Open pollygon has less than two vertices"
            self.add_line_segment(asset=asset, from_here=v1, to_there=v2)

    def add_polygon(self, asset: str, vertices: List[Position]):
        """
        Add a closed polygon as a sequence of Tablet coordinate vertices. Each vertex coordinate must be converted
        to a device coordinate.

        :param asset: Used to determine draw style
        :param vertices: Polygon vertices in tablet coordinates
        """
        # Flip each position to device coordinates
        device_vertices = [self.to_dc(v) for v in vertices]
        self.Polygons.append(_Polygon(
            vertices= device_vertices,
            border_style=StyleDB.shape_presentation[asset],
            fill=StyleDB.fill_style[asset]
        ))

    def add_rectangle(self, asset: str, lower_left: Position, size: Rect_Size):
        """
        Adds a rectangle to the tablet and converts the lower left corner to device coordinates
        """
        # Flip lower left corner to device coordinates
        ll_dc = self.to_dc(Position(x=lower_left.x, y=lower_left.y))

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # Check to see if this rectangle is filled
        fill = StyleDB.fill_style.get(asset, None)

        self.Rectangles.append(_Rectangle(
            upper_left=ul, size=size, border_style=StyleDB.shape_presentation[asset], fill=fill
        ))

    def add_text_line(self, asset: str, lower_left: Position, text: str):
        """
        Adds a line of text to the tablet at the specified lower left corner location which will be converted
        to device coordinates
        """
        self.Text.append(
            _Text_line(
                lower_left=self.to_dc(lower_left), text=text, style=StyleDB.text_presentation[asset]
            )
        )
        self.logger.info('Text added')

    def add_text_block(self, asset: str, lower_left: Position, text: List[str],
                       align: HorizAlign = HorizAlign.LEFT):
        """
        Add all lines of text to the tablet text render list each at the correct position
        on the tablet. Set the lower left x of each line based on right or left alignment
        within the text block.  Assuming left alignment as default.

        :param asset:  To get the text style
        :param lower_left: Lower left corner of the text block on the Tablet
        :param text: One or more lines of text
        :param align: Horizontal text alignment (left, right or center)
        """
        style_name = StyleDB.text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_height = style.size
        spacing = font_height*style.spacing

        # Get height of one line (any will do since they all use the same text style)
        xpos, ypos = lower_left  # Initialize at lower left corner
        x_indent = 0  # Assumption for left aligned block
        if align != HorizAlign.LEFT:
            # We'll need the total width of the block as a reference point
            longest_line = max(text, key=len)
            block_width = self.text_line_size(asset=asset, text_line=longest_line).width
        for line in text[::-1]:  # Reverse order since we are positioning lines from the bottom up
            # always zero indent from xpos when left aligned
            if align == HorizAlign.RIGHT:
                line_width = self.text_line_size(asset=asset, text_line=line).width
                x_indent = block_width - line_width  # indent past xpos by the difference
            if align == HorizAlign.CENTER:
                line_width = self.text_line_size(asset=asset, text_line=line).width
                x_indent = (block_width - line_width) / 2  # indent 1/2 of non text span
            self.add_text_line(asset=asset, lower_left=Position(xpos+x_indent, ypos), text=line)
            ypos += spacing

    def render_rects(self):
        """Draw the rectangle shapes"""
        for r in self.Rectangles:
            # Set the dash pattern
            pname = StyleDB.line_style[r.border_style].pattern  # name of border line style's pattern
            pvalue = StyleDB.dash_pattern[pname]  # find pattern value in dash pattern dict
            self.Context.set_dash(pvalue)  # If pvalue is [], line will be solid
            # Set color and width
            line_color_name = StyleDB.line_style[r.border_style].color
            line_rgb_color_value = StyleDB.rgbF[line_color_name]
            if r.fill:
                fill_rgb_color_value = StyleDB.rgbF[r.fill]
            w = StyleDB.line_style[r.border_style].width
            self.Context.set_line_width(w)
            # Set rectangle extents and draw
            self.Context.rectangle(r.upper_left.x, r.upper_left.y, r.size.width, r.size.height)
            if r.fill:
                self.Context.set_source_rgb(*fill_rgb_color_value)
                self.Context.fill_preserve()
            self.Context.set_source_rgb(*line_rgb_color_value)
            self.Context.stroke()

    def render_line_segments(self):
        """Draw the line segments"""
        for l in self.Line_segments:
            # Set the dash pattern
            pname = StyleDB.line_style[l.style].pattern  # name of line style's pattern
            pvalue = StyleDB.dash_pattern[pname]  # find pattern value in dash pattern dict
            self.Context.set_dash(pvalue)  # If pvalue is [], line will be solid
            # Set color and width
            cname = StyleDB.line_style[l.style].color
            c = StyleDB.rgbF[cname]
            self.Context.set_source_rgb(*c)
            w = StyleDB.line_style[l.style].width
            self.Context.set_line_width(w)
            # Set line segment and draw
            self.Context.move_to(*l.from_here)
            self.Context.line_to(*l.to_there)
            self.Context.stroke()

    def render_polygons(self):
        """Draw the closed non-rectangular shapes"""
        for p in self.Polygons:
            pattern_name = StyleDB.line_style[p.border_style].pattern  # name of border line style's pattern
            pattern_value = StyleDB.dash_pattern[pattern_name]  # find pattern value in dash pattern dict
            self.Context.set_dash(pattern_value)  # If pattern_value is [], line will be solid
            # Set color and width
            line_color_name = StyleDB.line_style[p.border_style].color
            line_rgb_color_value = StyleDB.rgbF[line_color_name]
            fill_rgb_color_value = StyleDB.rgbF[p.fill]
            w = StyleDB.line_style[p.border_style].width
            self.Context.set_line_width(w)
            # Draw a closed polygon
            self.Context.move_to(*p.vertices[0])  # Start drawing here
            for v in p.vertices[1:]:
                self.Context.line_to(*v)
            self.Context.close_path()
            self.Context.set_source_rgb(*fill_rgb_color_value)
            self.Context.fill_preserve()
            self.Context.set_source_rgb(*line_rgb_color_value)
            self.Context.stroke()

    def render_text(self):
        """Draw all text lines"""
        for t in self.Text:
            style = StyleDB.text_style[t.style]
            text_color_name = StyleDB.text_style[t.style].color
            text_rgb_color_value = StyleDB.rgbF[text_color_name]
            self.Context.set_source_rgb(*text_rgb_color_value)
            self.Context.select_font_face(
                style.typeface, Cairo_font_slant[style.slant], Cairo_font_weight[style.weight]
            )
            self.Context.set_font_size(style.size)
            self.Context.move_to(t.lower_left.x, t.lower_left.y)
            self.Context.show_text(t.text)

    def render(self):
        """Renders the tablet using Cairo for now"""

        # For now, always assume output to cairo
        self.Context.set_line_join(cairo.LINE_JOIN_ROUND)
        self.render_line_segments()
        self.render_rects()
        self.render_polygons()
        self.render_text()

    def text_block_size(self, asset: str, text_block: List[str]) -> Rect_Size:
        """
        Determines the dimensions of a rectangle bounding the text to be drawn.

        :param asset:
        :param text_block:
        :return:
        """
        style_name = StyleDB.text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_height = style.size
        spacing = font_height*style.spacing
        inter_line_spacing = spacing - font_height  # Space between two lines

        num_lines = len(text_block)
        assert num_lines > 0, "Text block size requested for empty text block"
        # The text block is the width of its widest ink render extent
        widths = [self.text_line_size(asset, line).width for line in text_block]
        widest_line = text_block[widths.index(max(widths))]
        block_width = self.text_line_size(asset=asset, text_line=widest_line).width
        block_height = num_lines*spacing - inter_line_spacing  # Deduct that one unneeded line of spacing on the top

        return Rect_Size(width=block_width, height=block_height)

    def text_line_size(self, asset: str, text_line: str) -> Rect_Size:
        """
        Returns the size of a line of text when rendered with the asset's text style
        :param asset: Application entity to determine text style
        :param text_line: Text that would be rendered
        :return: Size of the text line ink area
        """
        style_name = StyleDB.text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        # Configure the Cairo context with style properties and the text line
        self.Context.select_font_face(
            style.typeface, Cairo_font_slant[style.slant], Cairo_font_weight[style.weight],
        )
        self.Context.set_font_size(style.size)
        te = self.Context.text_extents(text_line)
        return Rect_Size(height=te.height, width=te.width)

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
        return f'Size: {self.Size}, Presentation: {self.Presentation}, drawing: {self.Drawing_type},' \
               f'Output: {self.Output_file}'
