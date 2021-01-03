"""
tablet_test.py - Verify that tablet works okay apart from the app
"""

from flatland.database.flatlanddb import FlatlandDB
from flatland.drawing_domain.tablet import Tablet
from flatland.datatypes.geometry_types import Rect_Size, Position

atext = ['ID : Nominal {I}', 'Grid {R10}', 'Type {R11, R30}', 'Notation {R30}',
         'Canvas {R14}', 'Size : Rect Size', 'Origin : Position', 'Presentation style {R26}']

stext = ['Diagram']

fdb = FlatlandDB()
t = Tablet(size=Rect_Size(height=8.5*72, width=11*72), output_file='tab_test.pdf',
           drawing_type='Starr class diagram', presentation='diagnostic')

# Create a large text compartment and draw a rectangle around it

block_size = t.text_block_size(asset='attributes', text_block=atext)
pad_block_size = Rect_Size(height=block_size.height+14, width=block_size.width)
t.add_rectangle(asset='class compartment', lower_left=Position(100, 100), size=pad_block_size)

t.add_text_block(asset='attributes', lower_left=Position(110,110), text=atext)


# t.add_text_line(asset='attributes', text='Altitude : MSL', lower_left=Position(106, 50 + leading))

# arrow_points = [Position(200,203.5), Position(209,200), Position(200,196.5)]
# t.add_polygon(asset='solid arrow', vertices=arrow_points)
# bend_points = [Position(200, 300), Position(300, 300), Position(300, 400)]
# t.add_open_polygon(asset='binary association connector', vertices=bend_points)
t.render()
print(t)