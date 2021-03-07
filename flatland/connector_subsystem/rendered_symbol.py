"""
rendered_symbol.py
"""
import logging
from flatland.datatypes.geometry_types import Position
from flatland.datatypes.connection_types import NodeFace, OppositeFace
from flatland.decoration_subsystem.symbol import Symbol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flatland.connector_subsystem.stem import Stem
    from flatland.drawing_domain.layer import Layer


class RenderedSymbol:
    """
    Take a position for placement x,y
    Look up symbol point data, choosing appropriate rotation if not a circle
    Translate coordinates by adding to x,y position
    Draw open polygon and supply to tablet with asset name
    """

    def __init__(self, stem: 'Stem', end: str, location: Position, symbol_name: str):
        self.logger = logging.getLogger(__name__)
        self.Symbol_spec = Symbol.instances[symbol_name]
        self.Symbol_name = symbol_name
        self.Stem = stem
        self.End = end
        self.Growth = 0

        layer = self.Stem.Connector.Diagram.Layer

        if self.Symbol_spec.type != 'compound':
            self.draw_simple_symbol(layer=layer, symbol_name=self.Symbol_name, location=location)
        else:
            stack = self.Symbol_spec.spec
            next_location = location  # Start at the original location
            for s in stack:
                self.logger.info(f'NEXT LOCATION: {next_location}')
                if s.type == 'arrow':
                    next_location = self.draw_arrow(layer=layer, arrow_symbol=s.symbol, location=next_location)

    def draw_simple_symbol(self, layer: 'Layer', symbol_name: str, location: Position):
        """ Draw any simple symbol at the indicated location """
        if self.Symbol_spec.type == 'arrow':
            self.draw_arrow(layer, arrow_symbol=symbol_name, location=location)
        else:
            # TODO: Support all of the Decorator subsystem symbols
            assert False, f'Symbol: {self.Symbol_name} not supported yet.'

    def draw_arrow(self, layer: 'Layer', arrow_symbol: str, location: Position) -> Position:
        """Draw an arrow symbol at the indicated location pointing toward our face"""
        # Get the numpy polygon matrix with the rotation pointing toward the Node face
        orientation = self.Stem.Node_face  # Will not work for a tertiary stem!
        if self.End == 'vine':
            # reverse orientation since the vine symbol points away from the node face
            orientation = OppositeFace[orientation]

        rotated_arrow = Symbol.instances[arrow_symbol].spec.shape.rotations[orientation]
        # Add the coordinates to our location
        vertices = [Position(location.x + x, location.y + y) for x, y in rotated_arrow]
        layer.add_polygon(asset=arrow_symbol, vertices=vertices)
        offset = Symbol.instances[arrow_symbol].length
        # TODO: Growth needs to be updated regardless of symbol type (not just arrow)
        self.Growth += offset
        if orientation == NodeFace.TOP:
            return Position(location.x, location.y+offset)
        elif orientation == NodeFace.BOTTOM:
            return Position(location.x, location.y-offset)
        elif orientation == NodeFace.LEFT:
            return Position(location.x-offset, location.y)
        elif orientation == NodeFace.RIGHT:
            return Position(location.x+offset, location.y)
