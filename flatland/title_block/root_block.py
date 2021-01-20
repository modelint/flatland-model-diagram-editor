"""root_block.py - Rectangular block that envelopes title block information"""

from flatland.drawing_domain.tablet import Tablet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.node_subsystem.canvas import Canvas



class RootBlock:
    """
    Rectangular block that envelopes title block information

    """
    Width =  400
    Height = 200

    def __init__(self, canvas: 'Canvas'):
        """
        Constructor
        """
        self.Canvas = canvas

    def render(self):
        """Draw self"""

