"""
sheet.py – The canvas is drawn on this instance of sheet
"""

from sqlalchemy import select
from flatland.flatland_exceptions import UnknownSheetSize, UnknownSheetGroup
from flatland.database.flatlanddb import FlatlandDB as fdb
from flatland.datatypes.geometry_types import Rect_Size
from enum import Enum


class Group(Enum):
    US = 0
    INT = 1


class Sheet:
    """
    A US or international standard sheet size.

        Attributes

        - Name -- A name like A3, tabloid, letter, D, etc
        - Group -- Either *us* or *int* to distinguish between measurement units
        - Size --  Sheet dimensions float since us has 8.5 x 11 or int for international mm units
        - Size_group -- Sheet Size Groups are used to determine the scaling for each available Title Block Pattern.

          Roughly similar sizes such as Letter, A4 and Legal may be grouped together in the same Sheet Size Group
          since the same Title Block scale will work for all three sizes.

          Since any Sheet must specify a scale to be used for any Title Block Patterns, each Sheet must be categorized
          in a Sheet Size Group.
    """
    def __init__(self, name: str):
        """
        Constructor

        :param name:  A standard sheet name in our database such as letter, tabloid, A3, etc
        """
        sheet_t = fdb.MetaData.tables['Sheet']
        query = select([sheet_t]).where(sheet_t.c.Name == name)
        i = fdb.Connection.execute(query).fetchone()
        if not i:
            raise UnknownSheetSize(name)
        self.Name = name
        self.Size_group = i['Size group']
        if i.Group == 'us':
            self.Group = Group.US
        elif i.Group == 'int':
            self.Group = Group.INT
        else:
            raise UnknownSheetGroup("Group: [{i.Group}]")

        if self.Group == Group.US:
            self.Size = Rect_Size(height=float(i.Height), width=float(i.Width))
        else:
            self.Size = Rect_Size(height=int(i.Height), width=int(i.Width))

    def __repr__(self):
        return f'Sheet({self.Name})'

    def __str__(self):
        u = "in" if self.Group == Group.US else 'mm'
        return f'{self.Name} ({self.Size_group}): H{self.Size.height} {u} x W{self.Size.width} {u}'
