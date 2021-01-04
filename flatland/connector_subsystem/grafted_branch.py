"""
grafted_branch.py
"""
from flatland.connector_subsystem.branch import Branch
from flatland.connector_subsystem.anchored_tree_stem import AnchoredTreeStem
from typing import Set, TYPE_CHECKING
from flatland.datatypes.connection_types import Orientation, HorizontalFace
from flatland.connector_subsystem.floating_leaf_stem import FloatingLeafStem
from flatland.datatypes.geometry_types import Line_Segment, Position
from flatland.datatypes.general_types import Index
from flatland.datatypes.command_interface import New_Stem

if TYPE_CHECKING:
    from flatland.connector_subsystem.tree_connector import TreeConnector


class GraftedBranch(Branch):
    """
    This is a Branch positioned by grafting it to a designated Anchored Tree Stem

        Attributes

        Relationships

        - Grafting_stem -- The Anchored Tree Stem that grafts (sets the position of) this branch,
          R157 on the class model
        - Connector -- The Tree Connector of this Branch


    """

    def __init__(self, order: Index, connector: 'TreeConnector', hanging_stems: Set[AnchoredTreeStem],
                 grafting_stem: AnchoredTreeStem, new_floating_stem: New_Stem):
        """
        Constructor

        Given a user specifiction for the floating stem (a stem that is positioned by a grafting stem),
        we unpack it into a Floating Leaf Stem object and position it using the Grafted Branch's grafting
        Anchored Tree Stem.

        :param order: This Branches order in the draw sequence
        :param connector: Our Tree Connector
        :param hanging_stems: (AnchoredTreeStems)
        :param grafting_stem: (AnchoredTreeStem)
        :param new_floating_stem: (New_Stem) We are given the user specification of this Stem
        """

        self.Grafting_stem = grafting_stem
        self.Connector = connector

        # Set the branch axis based on the graft stem x or y depending on face orientation
        if self.Grafting_stem.Node_face in HorizontalFace:
            axis = grafting_stem.Root_end.x
            axis_orientation = Orientation.Vertical
        else:
            axis = grafting_stem.Root_end.y
            axis_orientation = Orientation.Horizontal

        # Unpack any Floating Stem
        self.Floating_stem = None if not new_floating_stem else self.unpack_floating_leaf(
            new_floating_leaf=new_floating_stem, grafting_stem=grafting_stem,
            axis_orientation=axis_orientation, axis=axis)

        Branch.__init__(self, order=order, axis=axis, connector=connector, hanging_stems=hanging_stems,
                        axis_orientation=axis_orientation)

    def unpack_floating_leaf(self, new_floating_leaf, grafting_stem,
                             axis_orientation, axis) -> FloatingLeafStem:
        """
        Extract data in user supplied New_Stem named tuple and use it to create a FloatingLeafStem object.

        :param new_floating_leaf:
        :param grafting_stem:
        :param axis_orientation:
        :param axis:
        :return:
        """
        if axis_orientation == Orientation.Horizontal:
            x = new_floating_leaf.node.Face_position(new_floating_leaf.face)
            y = axis
        else:
            x = axis
            y = new_floating_leaf.node.Face_position(new_floating_leaf.face)
        root_position = Position(x, y)

        # Lookup the StemType object
        leaf_stem_type = self.Connector.Connector_type.Stem_type[new_floating_leaf.stem_type]
        return FloatingLeafStem(
            connector=self.Connector,
            stem_type=leaf_stem_type,
            semantic=new_floating_leaf.semantic,
            node=new_floating_leaf.node,
            face=new_floating_leaf.face,
            grafted_branch=grafting_stem,
            root_position=root_position,
            name=None
        )

    @property
    def Shoot(self) -> Line_Segment:
        """
        The Shoot is simply a line segment from the vine end of the grafting Anchored Tree Stem to the
        vine end of the Floating Leaf Stem
        :return: The line segment to draw
        """
        if self.Floating_stem:
            return Line_Segment(from_position=self.Grafting_stem.Root_end, to_position=self.Floating_stem.Root_end)
        else:
            return super().Shoot
