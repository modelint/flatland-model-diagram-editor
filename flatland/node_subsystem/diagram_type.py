"""
diagram_type.py - Diagram Type
"""
from flatland.node_subsystem.node_type import NodeType
from flatland.datatypes.geometry_types import Rect_Size
from flatland.connector_subsystem.connector_type import ConnectorType
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_


class DiagramType:
    """
    A standard diagram such as ‘class diagram’, ‘state machine diagram’ or ‘collaboration diagram’. Each of these
    types draws certain kinds of Nodes and Connectors supported by one or more standard Notations.

        Attributes

        - Name -- A descriptive name of this Diagram Type

        Relationships

        - R15 / Node types -- All Node Types defined on this Diagram Type
        - R50 / Connector types -- All Connector Types defined on this Diagram Type
    """

    def __init__(self, name: str, notation: str):
        """
        Constructor – Loads this Diagrams type data from the database

        :param name:  User selected Diagram Type name
        :param notation:  User selected Notation name
        """
        self.Name = name
        self.NodeTypes = {}
        self.ConnectorTypes = {}

        # Load Node and Compartment Types for this
        ntypes_t = fdb.MetaData.tables['Node Type']
        p_q = [ntypes_t.c.Name, ntypes_t.c.About, ntypes_t.c['Default height'], ntypes_t.c['Default width'],
               ntypes_t.c['Max height'], ntypes_t.c['Max width']]
        r_q = and_(ntypes_t.c['Diagram type'] == self.Name)
        q = select(p_q).where(r_q)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            self.NodeTypes[r.Name] = NodeType(
                name=r['Name'], diagram_type_name=self.Name, about=r.About,
                default_size=Rect_Size(height=r['Default height'], width=r['Default width']),
                max_size=Rect_Size(height=r['Max height'], width=r['Max width'])
            )

        # Load Connector types on model relationship R50
        ctypes_t = fdb.MetaData.tables['Connector Type']
        p = [ctypes_t.c.Name, ctypes_t.c.About, ctypes_t.c.Geometry]
        r = and_(ctypes_t.c['Diagram type'] == self.Name)
        q = select(p).where(r)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            self.ConnectorTypes[r.Name] = ConnectorType(
                name=r.Name, diagram_type_name=self.Name, about=r.About, geometry=r.Geometry, notation=notation
            )

    def __str__(self):
        return self.Name
