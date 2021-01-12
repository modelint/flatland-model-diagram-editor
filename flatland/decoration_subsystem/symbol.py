"""
symbol.py - Symbols from the Decoration Subsystem, loaded from the database
"""
from flatland.datatypes.geometry_types import Position
from flatland.datatypes.connection_types import NodeFace
from sqlalchemy import select, join, func, and_
from collections import namedtuple
from flatland.database.flatlanddb import FlatlandDB as fdb
from typing import Dict
import numpy as np


# Symbol subclasses in the Decoration Subsystem are implemented as named tuples
# See Decoration Subsystem class model descriptions for full details on named tuple attributes summarized here

SymbolSpec = namedtuple('Symbol', 'length type spec')
"""
Symbol

- length -- extent of the drawn symbol along a connector's axis
- type -- subclass of simple symbol or compound, e.g. 'arrow, circle, cross, compound'
- spec -- the shape definition via R103 on the class diagram
"""

SimpleSymbol = namedtuple('SimpleSymbol', 'terminal_offset shape')
"""
Simple Symbol

- terminal_offset -- distance away from root or vine end
- shape -- shape specific definition via R100 on the class diagram
"""

StackPlacement = namedtuple('StackPlacement', 'symbol type arrange offset')
"""
Symbol Stack Placement

The placement of a Simple Symbol within a Compound Symbol
A sequence of these constitues the spec for a Compound Symbol

- symbol -- Name of a Simple Symbol positioned in the stack
- type -- Type of the Simple Symbol positioned in the stack
- arrange -- layered on top or adjacent to the previous Simple Symbol in the stack
- offset -- positional offset from the center if layered or side if adjacent
"""

# Simple Symbol shape specific attributes
ArrowSymbol = namedtuple('ArrowSymbol', 'half_base height fill rotations')
CircleSymbol = namedtuple('CircleSymbol', 'radius solid')
CrossSymbol = namedtuple('CrossSymbol', 'root_offset vine_offset width angle')
# TODO: Add rotations for Cross symbol as well


# TODO: For each Arrow Symbol we need to compute the points of a polygon facing upward
# TODO: Then we apply a rotation matrix to get each of the other 90 deg orientations and store
# TODO: Those indexed by node face
# TODO: https://www.varsitytutors.com/hotmath/hotmath_help/topics/transformation-of-graphs-using-matrices-rotations

r90 = np.array([ [0, 1], [-1, 0] ])
r180 = np.array([ [-1, 0], [0, -1] ])
r270 = np.array([ [0, -1], [1, 0] ])


class Symbol:
    """
    All Symbols are loaded from the database and held in the instances dictionary keyed by Symbol.Name
    """
    instances = {}

    def __init__(self, diagram_type: str, notation: str):
        """
        Load all symbols used on this diagram type for this notation

        :param diagram_type:
        :param notation:
        """
        self.update_symbol_lengths()

        # Tables
        sdecs_t = fdb.MetaData.tables['Stem End Decoration']
        arrow_t = fdb.MetaData.tables['Arrow Symbol']
        circle_t = fdb.MetaData.tables['Circle Symbol']
        cross_t = fdb.MetaData.tables['Cross Symbol']
        symbol_t = fdb.MetaData.tables['Symbol']
        s_symbol_t = fdb.MetaData.tables['Simple Symbol']
        stackp_t = fdb.MetaData.tables['Symbol Stack Placement']

        f = and_(
            (sdecs_t.c['Diagram type'] == diagram_type),
            (sdecs_t.c['Notation'] == notation)
        )
        # Simple symbols
        # Arrow symbols
        p = [symbol_t.c.Name, symbol_t.c.Length, s_symbol_t.c['Terminal offset'], arrow_t.c['Half base'], arrow_t.c.Height,
             arrow_t.c.Fill]
        j = sdecs_t.join(symbol_t, sdecs_t.c.Symbol == symbol_t.c.Name).join(s_symbol_t).join(arrow_t)
        q = select(p).select_from(j).where(f)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            rotations = Symbol.compute_arrow_rotations(r['Half base'], r.Height)
            Symbol.instances[r.Name] = SymbolSpec(
                length=r.Length,
                type='arrow',
                spec=SimpleSymbol(
                    terminal_offset=r['Terminal offset'],
                    shape=ArrowSymbol(half_base=r['Half base'], height=r.Height, fill=r.Fill, rotations=rotations)
                ),
            )
        # Circle symbols
        p = [symbol_t.c.Name, symbol_t.c.Length, s_symbol_t.c['Terminal offset'], circle_t.c.Radius, circle_t.c.Solid]
        j = sdecs_t.join(symbol_t, sdecs_t.c.Symbol == symbol_t.c.Name).join(s_symbol_t).join(circle_t)
        q = select(p).select_from(j).where(f)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            Symbol.instances[r.Name] = SymbolSpec(
                length=r.Length,
                type='circle',
                spec=SimpleSymbol(
                    terminal_offset=r['Terminal offset'],
                    shape=CircleSymbol(radius=r.Radius, solid=r.Solid)
                ),
            )
        # Cross symbols
        p = [symbol_t.c.Name, symbol_t.c.Length, s_symbol_t.c['Terminal offset'],
             cross_t.c['Root offset'], cross_t.c['Vine offset'], cross_t.c.Width, cross_t.c.Angle]
        j = sdecs_t.join(symbol_t, sdecs_t.c.Symbol == symbol_t.c.Name).join(s_symbol_t).join(cross_t)
        q = select(p).select_from(j).where(f)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            Symbol.instances[r.Name] = SymbolSpec(
                length=r.Length,
                type='cross',
                spec=SimpleSymbol(
                    terminal_offset=r['Terminal offset'],
                    shape=CrossSymbol(
                        root_offset=r['Root offset'], vine_offset=r['Vine offset'], width=r.Width, angle=r.Angle
                    )
                ),
            )

        # Compound symbols
        p = [symbol_t.c.Name, symbol_t.c.Length, stackp_t.c.Position, stackp_t.c['Simple symbol'],
             stackp_t.c.Arrange, stackp_t.c['Offset x'], stackp_t.c['Offset y']]
        j = sdecs_t.join(symbol_t, sdecs_t.c.Symbol == symbol_t.c.Name).join(
            stackp_t, symbol_t.c.Name == stackp_t.c['Compound symbol'])
        q = select(p).select_from(j).distinct().where(f).order_by("Name", "Position")
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            # Determine the type of the Simple Symbol positioned within the stack
            # Must be one of the Simple Symbol subclass names and not 'compound' or anything else
            simple_symbol_type = self.instances[r['Simple symbol']].type
            assert simple_symbol_type in ('arrow', 'circle', 'cross'), "Bad type for simple symbol in stack"
            if r.Position == 1:  # First item of new stack
                # Start a new stack of simple symbols
                stack = [StackPlacement(
                    symbol=r['Simple symbol'], type=simple_symbol_type,
                    arrange=r.Arrange, offset=Position(r['Offset x'], r['Offset y'])
                )]
            else:
                # We don't neeed the terminating arrange value in a list
                arrange = r.Arrange if r.Arrange not in ('top', 'last') else None
                # Put the simple symbol on the stack using this clipped arrange value
                stack.append( StackPlacement(
                    symbol=r['Simple symbol'], type=simple_symbol_type,
                    arrange=arrange,  offset=Position(r['Offset x'], r['Offset y']))
                )
                if not arrange:
                    # No more simple symbols on this stack, so add the compound symbol to the instance dict
                    Symbol.instances[r.Name] = SymbolSpec(length=r.Length, type='compound', spec=stack[:])  # COPY the stack

    @staticmethod
    def compute_arrow_rotations( half_base: int, height: int ) -> Dict[ NodeFace, np.ndarray ]:
        """
        Create a dictionary of arrow polygons each rotated 90 degree rotations and keyed to the appropriate
        Node Face orientation where the arrow head would attach or point toward the face.
        system with 0,0 at the arrow head.

        :param half_base:  1/2 the arrow triangle base
        :param height: height of the arrow triangle
        :return: dictionary of all four arrow rotations, one per node face
        """
        # Prior to rotation each row is a set of coordinates on the same dimension (x or y)
        bottom_arrow = np.array([[0, half_base, -half_base], [0, -height, -height]])  # x values, y values
        rotations = {
            NodeFace.BOTTOM: bottom_arrow,
            NodeFace.LEFT: np.dot(r90, bottom_arrow),
            NodeFace.TOP: np.dot(r180, bottom_arrow),
            NodeFace.RIGHT: np.dot(r270, bottom_arrow)
        }
        # Now that the rotate operations are complete, return a flipped matrix
        # so that each row is a coordinate pair using the numpy reshape operation
        for k,v in rotations.items():
            rotations[k] = [Position(z[0],z[1]) for z in zip(v[0],v[1])]
        return rotations

    @staticmethod
    def update_symbol_lengths():
        """
        Symbol.Length is a derived attribute in the Decoration Subsystem class model
        Compute total drawn length along Connector axis for each Symbol and update the database
        """
        # Simple Symbols first
        arrow_t = fdb.MetaData.tables['Arrow Symbol']
        circle_t = fdb.MetaData.tables['Circle Symbol']
        cross_t = fdb.MetaData.tables['Cross Symbol']
        symbol_t = fdb.MetaData.tables['Symbol']

        query = select([symbol_t]).where(symbol_t.c.Shape != 'compound')
        simple_symbols = fdb.Connection.execute(query).fetchall()
        for ssym in simple_symbols:
            if ssym.Shape == 'arrow':
                query = select([arrow_t.c.Height]).where(arrow_t.c.Name == ssym.Name)
                v = fdb.Connection.execute(query).scalar()
                u = symbol_t.update().where(symbol_t.c.Name == ssym.Name).values(Length=v)
                fdb.Connection.execute(u)
            if ssym.Shape == 'circle':
                query = select([circle_t.c.Radius]).where(circle_t.c.Name == ssym.Name)
                v = 2 * fdb.Connection.execute(query).scalar()
                u = symbol_t.update().where(symbol_t.c.Name == ssym.Name).values(Length=v)
                fdb.Connection.execute(u)
            if ssym.Shape == 'cross':
                query = select([cross_t.c['Root offset'], cross_t.c['Vine offset']]).where(cross_t.c.Name == ssym.Name)
                result = fdb.Connection.execute(query).fetchone()
                v = result['Root offset'] + result['Vine offset']
                u = symbol_t.update().where(symbol_t.c.Name == ssym.Name).values(Length=v)
                fdb.Connection.execute(u)

        # Compound symbols
        # We want the sum for side-by-side simple symbols and the max for vertically stacked symbols
        splace_t = fdb.MetaData.tables['Symbol Stack Placement']
        j = join(symbol_t, splace_t, splace_t.c['Simple symbol'] == symbol_t.c.Name)
        q = select(  # simple symbol inclusions in adjacency arrangement, compound, simple, length
            [splace_t.c['Compound symbol'], splace_t.c['Simple symbol'], symbol_t.c.Length,
             func.sum(symbol_t.c.Length).label("Total")]
        ).select_from(j).where(splace_t.c.Arrange.in_(['adjacent', 'last'])).group_by(splace_t.c['Compound symbol'])
        found = fdb.Connection.execute(q).fetchall()
        for r in found:
            u = symbol_t.update().where(symbol_t.c.Name == r['Compound symbol']).values(Length=r.Total)
            fdb.Connection.execute(u)

        q = select(  # simple symbol inclusions in adjacency arrangement, compound, simple, length
            [splace_t.c['Compound symbol'], splace_t.c['Simple symbol'], symbol_t.c.Length,
             func.max(symbol_t.c.Length).label("Max")]
        ).select_from(j).where(splace_t.c.Arrange.in_(['layer', 'top'])).group_by(splace_t.c['Compound symbol'])
        found = fdb.Connection.execute(q).fetchall()
        for r in found:
            u = symbol_t.update().where(symbol_t.c.Name == r['Compound symbol']).values(Length=r.Max)
            fdb.Connection.execute(u)


if __name__ == "__main__":
    fdb()
    Symbol.update_symbol_lengths()
    starr = 'Starr'
    sm = 'Shlaer-Mellor'
    x = 'xUML'
    smd = 'state machine'
    cd = 'class'
    s = Symbol(diagram_type=cd, notation=starr)
