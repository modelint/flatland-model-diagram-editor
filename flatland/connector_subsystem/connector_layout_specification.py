"""
connector_layout_specification.py – Connector Layout Specification
"""

from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select


class ConnectorLayoutSpecification:
    """
    Defines a set of values that determine how a Connector is drawn.

        Attributes

        - Default_stem_positions -- The number of equally spaced positions relative to a center position (included in
          the count) on a Node face where a Stem can be attached. A value of one corresponds to a single connection
          point in the center of a Node face. A value of three is a central connection point with one on either side,
          and so on. In practice, five is usually the # right number, especially for a class or state diagram. But this
          could vary by diagram and node type in the future.
        - Default_rut_positions -- The number of ruts where Path can be defined in a Lane. These work like stem/anchor
          positions on a Lane as opposed to a Node face. For a value of 3 we get positions -1, 0 and +1 with
          0 representing the Lane Center # and +1 high/right and -1 low/left.
        - Runaround_lane_width -- TODO: Verify that this is depcrecated (replaced by two items below)
        - Default_new_path_row_height -- When adding an empty row to acommodate a Path in a Connector use this height
        - Default_new_path_col_width -- When adding an empty col to acommodate a Path in a Connector use this width
        - Default_unary_branch_length -- The distance from the root end on the Node face to the vine end just before
          any vine end shape decorations are drawn
    """
    Default_stem_positions = None
    Default_rut_positions = None
    Runaround_lane_width = None
    Default_new_path_row_height = None
    Default_new_path_col_width = None
    Default_unary_branch_length = None

    def __init__(self):
        spec = fdb.MetaData.tables['Connector Layout Specification']
        q = select([spec])
        i = fdb.Connection.execute(q).fetchone()
        assert i, "No Connector Layout Specification in database"

        ConnectorLayoutSpecification.Default_stem_positions = i['Default stem positions']
        ConnectorLayoutSpecification.Default_rut_positions = i['Default rut positions']
        ConnectorLayoutSpecification.Runaround_lane_width = i['Runaround lane width']
        ConnectorLayoutSpecification.Default_new_path_row_height = i['Default new path row height']
        ConnectorLayoutSpecification.Default_new_path_col_width = i['Default new path col width']
        ConnectorLayoutSpecification.Default_unary_branch_length = i['Default unary branch length']
