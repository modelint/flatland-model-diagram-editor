"""
layer.py - A layer of graphics drawn on a Tablet
"""
import logging
from typing import List
import cairo
from flatland.drawing_domain.styledb import StyleDB
import flatland.drawing_domain.element as element
from flatland.datatypes.geometry_types import Rect_Size, Position, HorizAlign
from flatland.drawing_domain.presentation import  Presentation
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.drawing_domain.tablet import Tablet

Cairo_font_weight = {'normal': cairo.FontWeight.NORMAL, 'bold': cairo.FontWeight.BOLD}
"""Maps an application style to a cairo specific font weight"""
Cairo_font_slant = {'normal': cairo.FontSlant.NORMAL, 'italic': cairo.FontSlant.ITALIC}
"""Maps an application style to a cairo specific font slant"""


class Layer:
    """
    A common feature of many drawing and image editing applications is the ability to stack layers of
    content along a z axis toward the user’s viewpoint. Similarly, the Tablet renders each layer working
    from the lowest value on the z axis toward the highest. Thus, content on the higher layers may overlap
    content underneath.

        Attributes

        - Line_segments -- A list of geometric lines each with start and end coordinates.
        - Rectangles -- A list of rectangles each with a lower left corner, height and width
        - Polygons -- A list of closed polygons
        - Text -- A list of text lines (new lines are not supported)
    """

    def __init__(self, name: str, tablet: 'Tablet', presentation: str, drawing_type: str):
        """
        Constructor

        :param name: The Layer name
        :param tablet: The Tablet object
        :param presentation: Presentation to be applied to this Layer
        :param drawing_type: The Presentation's Drawing Type
        """
        self.logger = logging.getLogger(__name__)
        self.Name = name
        self.Tablet = tablet
        self.Drawing_type = drawing_type

        # Stuff we will draw on the Layer
        self.Line_segments: List[element.Line_Segment] = []
        self.Polygons: List[element.Polygon] = []
        self.Rectangles: List[element.Rectangle] = []
        self.Text: List[element.Text_line] = []
        self.Images: List[element.Image] = []

        # Load this Layer's presentation assets if they haven't been already
        # Unique ID (see Tablet Subsystem class diagram) of a Presentation is both
        # its name and its Drawing Type name.  So we combine them to form the index
        pres_index = ':'.join([self.Drawing_type, presentation])
        self.Presentation = self.Tablet.Presentations.get(pres_index)
        if not self.Presentation:
            # It hasn't been loaded from the Flatland DB yet
            self.Presentation = Presentation(name=presentation, drawing_type=self.Drawing_type)
            self.Tablet.Presentations[pres_index] = self.Presentation


    def render(self):
        """Renders all Elements on this Layer"""

        # For now, always assume output to cairo
        self.Tablet.Context.set_line_join(cairo.LINE_JOIN_ROUND)
        # Rendering order determines what can potentially overlap on this Layer, so order matters
        self.render_line_segments()
        self.render_rects()
        self.render_polygons()
        self.render_text()  # Render text after vector content so that it is never underneath
        self.render_images()  # Text should not be drawn over images, so we can render these last

    def add_text_line(self, asset: str, lower_left: Position, text: str, underlay_asset: str = None):
        """
        Adds a line of text to the tablet at the specified lower left corner location which will be converted
        to device coordinates
        """
        if underlay_asset:
            # We will draw the underlay asset underneath the text (probably a blank rectangle)
            tl_size = self.text_line_size(asset=asset, text_line=text)
            underlay_size = Rect_Size(height=tl_size.height+5, width=tl_size.width+5)
            underlay_pos = Position(lower_left.x-2, lower_left.y-3)
            self.add_rectangle(asset=underlay_asset, lower_left=underlay_pos, size=underlay_size)
        self.Text.append(
            element.Text_line(
                lower_left=self.Tablet.to_dc(lower_left), text=text,
                style=self.Presentation.Text_presentation[asset],
            )
        )
        self.logger.info('Text added')

    def text_line_size(self, asset: str, text_line: str) -> Rect_Size:
        """
        Returns the size of a line of text when rendered with the asset's text style
        :param asset: Application entity to determine text style
        :param text_line: Text that would be rendered
        :return: Size of the text line ink area
        """
        style_name = self.Presentation.Text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        # Configure the Cairo context with style properties and the text line
        self.Tablet.Context.select_font_face(
            style.typeface, Cairo_font_slant[style.slant], Cairo_font_weight[style.weight],
        )
        self.Tablet.Context.set_font_size(style.size)
        te = self.Tablet.Context.text_extents(text_line)
        return Rect_Size(height=te.height, width=te.width)

    def text_block_size(self, asset: str, text_block: List[str]) -> Rect_Size:
        """
        Determines the dimensions of a rectangle bounding the text to be drawn.

        :param asset:
        :param text_block:
        :return:
        """
        style_name = self.Presentation.Text_presentation[asset]  # Look up the text style for this asset
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
        style_name = self.Presentation.Text_presentation[asset]  # Look up the text style for this asset
        style = StyleDB.text_style[style_name]
        font_height = style.size
        spacing = font_height*style.spacing

        # Get height of one line (any will do since they all use the same text style)
        xpos, ypos = lower_left  # Initialize at lower left corner
        x_indent = 0  # Assumption for left aligned block
        block_width = None
        if align != HorizAlign.LEFT:
            # We'll need the total width of the block as a reference point
            longest_line = max(text, key=len)
            block_width = self.text_line_size(asset=asset, text_line=longest_line).width
        for line in text[::-1]:  # Reverse order since we are positioning lines from the bottom up
            # always zero indent from xpos when left aligned
            if align == HorizAlign.RIGHT:
                assert block_width, "block_width not set"
                line_width = self.text_line_size(asset=asset, text_line=line).width
                x_indent = block_width - line_width  # indent past xpos by the difference
            if align == HorizAlign.CENTER:
                line_width = self.text_line_size(asset=asset, text_line=line).width
                x_indent = (block_width - line_width) / 2  # indent 1/2 of non text span
            self.add_text_line(asset=asset, lower_left=Position(xpos+x_indent, ypos), text=line)
            ypos += spacing

    def add_line_segment(self, asset: str, from_here: Position, to_there: Position):
        """
        Convert line segment coordinates to device coordinates and combine with the Line Style defined
        for the Asset in the selected Preentation Style
        :param asset:
        :param from_here:
        :param to_there:
        """
        self.Line_segments.append(
            element.Line_Segment(from_here=self.Tablet.to_dc(from_here), to_there=self.Tablet.to_dc(to_there),
                                 style=self.Presentation.Shape_presentation[asset])
        )

    def add_image(self, resource_path: Path, lower_left: Position, size: Rect_Size):
        """
        Adds the image

        :param size:
        :param resource_path: Path to an image file
        :param lower_left:  Lower left corner of the image in Cartesian coordinates
        """
        # Flip lower left corner to device coordinates
        ll_dc = self.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # Add it to the list
        self.Images.append(element.Image(resource_path=resource_path, upper_left=ul, size=size))
        self.logger.info(f'Drawing>> Layer {self.Name} registered resource at: {resource_path}')

    def add_rectangle(self, asset: str, lower_left: Position, size: Rect_Size):
        """
        Adds a rectangle to the tablet and converts the lower left corner to device coordinates
        """
        # Flip lower left corner to device coordinates
        ll_dc = self.Tablet.to_dc(Position(x=lower_left.x, y=lower_left.y))

        # Use upper left corner instead
        ul = Position(x=ll_dc.x, y=ll_dc.y - size.height)

        # Check to see if this rectangle is filled
        fill = self.Presentation.Closed_shape_fill.get(asset, None)

        self.Rectangles.append(element.Rectangle(
            upper_left=ul, size=size, border_style=self.Presentation.Shape_presentation[asset], fill=fill
        ))

    def add_polygon(self, asset: str, vertices: List[Position]):
        """
        Add a closed polygon as a sequence of Tablet coordinate vertices. Each vertex coordinate must be converted
        to a device coordinate.

        :param asset: Used to determine draw style
        :param vertices: Polygon vertices in tablet coordinates
        """
        # Flip each position to device coordinates
        device_vertices = [self.Tablet.to_dc(v) for v in vertices]
        self.Polygons.append(element.Polygon(
            vertices= device_vertices,
            border_style=self.Presentation.Shape_presentation[asset],
            fill=self.Presentation.Closed_shape_fill[asset]
        ))

    def add_open_polygon(self, asset: str, vertices: List[Position]):
        """
        Add all of the line segments necessary to draw the polygon to our list of line segments

        :param asset: Used to look up the line style
        :param vertices: A sequences of 2 or more vertices
        """
        for v1, v2 in zip(vertices, vertices[1:]):
            assert len(vertices) > 1, "Open pollygon has less than two vertices"
            self.add_line_segment(asset=asset, from_here=v1, to_there=v2)

    def render_text(self):
        """Draw all text lines"""
        for t in self.Text:
            style = StyleDB.text_style[t.style]
            text_color_name = StyleDB.text_style[t.style].color
            text_rgb_color_value = StyleDB.rgbF[text_color_name]
            self.Tablet.Context.set_source_rgb(*text_rgb_color_value)
            self.Tablet.Context.select_font_face(
                style.typeface, Cairo_font_slant[style.slant], Cairo_font_weight[style.weight]
            )
            self.Tablet.Context.set_font_size(style.size)
            self.Tablet.Context.move_to(t.lower_left.x, t.lower_left.y)
            self.Tablet.Context.show_text(t.text)

    def render_line_segments(self):
        """Draw the line segments"""
        for l in self.Line_segments:
            # Set the dash pattern
            pname = StyleDB.line_style[l.style].pattern  # name of line style's pattern
            pvalue = StyleDB.dash_pattern[pname]  # find pattern value in dash pattern dict
            self.Tablet.Context.set_dash(pvalue)  # If pvalue is [], line will be solid
            # Set color and width
            cname = StyleDB.line_style[l.style].color
            c = StyleDB.rgbF[cname]
            self.Tablet.Context.set_source_rgb(*c)
            w = StyleDB.line_style[l.style].width
            self.Tablet.Context.set_line_width(w)
            # Set line segment and draw
            self.Tablet.Context.move_to(*l.from_here)
            self.Tablet.Context.line_to(*l.to_there)
            self.Tablet.Context.stroke()

    def render_rects(self):
        """Draw the rectangle shapes"""
        for r in self.Rectangles:
            # Set the dash pattern
            pname = StyleDB.line_style[r.border_style].pattern  # name of border line style's pattern
            pvalue = StyleDB.dash_pattern[pname]  # find pattern value in dash pattern dict
            self.Tablet.Context.set_dash(pvalue)  # If pvalue is [], line will be solid
            # Set color and width
            line_color_name = StyleDB.line_style[r.border_style].color
            line_rgb_color_value = StyleDB.rgbF[line_color_name]
            fill_rgb_color_value = None if not r.fill else StyleDB.rgbF[r.fill]
            w = StyleDB.line_style[r.border_style].width
            self.Tablet.Context.set_line_width(w)
            # Set rectangle extents and draw
            self.Tablet.Context.rectangle(r.upper_left.x, r.upper_left.y, r.size.width, r.size.height)
            if r.fill:
                self.Tablet.Context.set_source_rgb(*fill_rgb_color_value)
                self.Tablet.Context.fill_preserve()
            self.Tablet.Context.set_source_rgb(*line_rgb_color_value)
            self.Tablet.Context.stroke()

    def render_polygons(self):
        """Draw the closed non-rectangular shapes"""
        for p in self.Polygons:
            pattern_name = StyleDB.line_style[p.border_style].pattern  # name of border line style's pattern
            pattern_value = StyleDB.dash_pattern[pattern_name]  # find pattern value in dash pattern dict
            self.Tablet.Context.set_dash(pattern_value)  # If pattern_value is [], line will be solid
            # Set color and width
            line_color_name = StyleDB.line_style[p.border_style].color
            line_rgb_color_value = StyleDB.rgbF[line_color_name]
            fill_rgb_color_value = StyleDB.rgbF[p.fill]
            w = StyleDB.line_style[p.border_style].width
            self.Tablet.Context.set_line_width(w)
            # Draw a closed polygon
            self.Tablet.Context.move_to(*p.vertices[0])  # Start drawing here
            for v in p.vertices[1:]:
                self.Tablet.Context.line_to(*v)
            self.Tablet.Context.close_path()
            self.Tablet.Context.set_source_rgb(*fill_rgb_color_value)
            self.Tablet.Context.fill_preserve()
            self.Tablet.Context.set_source_rgb(*line_rgb_color_value)
            self.Tablet.Context.stroke()

    def render_images(self):
        """Render all images"""
        for i in self.Images:
            image_surface = cairo.ImageSurface.create_from_png(i.resource_path)
            self.Tablet.Context.set_source_surface(image_surface, i.upper_left.x, i.upper_left.y)
            self.Tablet.Context.paint()

