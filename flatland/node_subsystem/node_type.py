"""
node_type.py
"""

from flatland.datatypes.geometry_types import Rect_Size, Padding, HorizAlign
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_
from collections import namedtuple

CompartmentType = namedtuple('CompartmentType', 'name alignment padding text_style')


class NodeType:
    def __init__(self, name: str, diagram_type_name: str, about: str, default_size: Rect_Size,
                 max_size: Rect_Size):
        """
        Constructor

        :param name:
        :param diagram_type_name:
        :param about:
        :param default_size:
        :param max_size:
        """
        self.Name = name
        self.About = about
        self.Default_size = default_size
        self.Max_size = max_size
        self.Diagram_type = diagram_type_name
        self.Compartment_types = []

        # Load Compartment types
        comptype_t = fdb.MetaData.tables['Compartment Type']
        r_p = [comptype_t.c.Name, comptype_t.c['Stack order'], comptype_t.c['Horizontal alignment'],
               comptype_t.c['Pad top'], comptype_t.c['Pad bottom'],
               comptype_t.c['Pad right'], comptype_t.c['Pad left'], comptype_t.c['Text style']
               ]
        r_q = and_(
            (comptype_t.c['Node type'] == self.Name),
            (comptype_t.c['Diagram type'] == self.Diagram_type)
        )
        q = select(r_p).where(r_q).order_by('Stack order')
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            self.Compartment_types.append( CompartmentType(
                name=r.Name,
                alignment=HorizAlign[r['Horizontal alignment']],
                padding=Padding(top=r['Pad top'], bottom=r['Pad bottom'], left=r['Pad left'], right=r['Pad right']),
                text_style=r['Text style'] )
            )

    def __repr__(self):
        return f'Name: {self.Name}, Default size: {self.Default_size}, Max size: {self.Max_size}'
