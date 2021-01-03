"""
connector_type.py - Connector Type
"""
from flatland.connector_subsystem.stem_type import StemType
from flatland.datatypes.connection_types import NameSpec, Buffer
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_


class ConnectorType:
    """
    One or more Nmodes may be interrelated by some model level relationship such as a state transition, generalization,
    association, dependency and so forth. Each such relationship is drawn with one or more connecting lines and
    terminating symbols.   A Connector Type defines the symbols, line connection geometry and appearance of Connectors
    corresponding to some model level relationship.

        Attributes

        - Name -- A descriptive name
        - Geometry -- The overall Connector branching layout corresponding to supported (modeled) Connector
          subclasses: *unary*, *binary* or *tree*

        Relationships

        - Stem_type / R59 -- Stem Types that appear on this Connector Type
        - Name_placement / R70 -- The Connector Name Placement Specification, if any, for our Notation

    """

    def __init__(self, name: str, diagram_type_name: str, about: str, geometry: str, notation: str):
        """
        Create all Stem Tnds for this Connector Type
        """
        self.Name = name
        self.Stem_type = {}
        self.Diagram_type = diagram_type_name
        self.About = about
        self.Geometry = geometry
        self.Name_spec = None

        # Load our name specification, if any, for the diagram type and notation
        name_spec_t = fdb.MetaData.tables['Name Spec']
        p = [name_spec_t.c['Vertical axis buffer'], name_spec_t.c['Horizontal axis buffer'],
             name_spec_t.c['Vertical end buffer'], name_spec_t.c['Horizontal end buffer'],
             name_spec_t.c['Default name'], name_spec_t.c.Optional]
        r = and_(
            (name_spec_t.c['Connector location'] == self.Name),
            (name_spec_t.c['Diagram type'] == diagram_type_name),
            (name_spec_t.c.Notation == notation)
        )
        q = select(p).where(r)
        r = fdb.Connection.execute(q).fetchone()
        if r:
            axis_buffer = Buffer(vertical=r['Vertical axis buffer'], horizontal=r['Horizontal axis buffer'])
            end_buffer = Buffer(vertical=r['Vertical end buffer'], horizontal=r['Horizontal end buffer'])
            self.Name_spec = NameSpec(axis_buffer=axis_buffer, end_buffer=end_buffer,
                                      default_name=r['Default name'], optional=r.Optional)

        # Load Stem types on model relationship R59
        stem_types_t = fdb.MetaData.tables['Stem Type']
        p = [stem_types_t.c.Name, stem_types_t.c.About, stem_types_t.c['Minimum length'], stem_types_t.c.Geometry]
        r = and_(
            (stem_types_t.c['Connector type'] == self.Name),
            (stem_types_t.c['Diagram type'] == diagram_type_name)
        )
        q = select(p).where(r)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            self.Stem_type[r.Name] = StemType(
                name=r.Name, connector_type_name=self.Name, diagram_type_name=self.Diagram_type,
                about=r.About, minimum_length=r['Minimum length'], geometry=r.Geometry, notation=notation)
