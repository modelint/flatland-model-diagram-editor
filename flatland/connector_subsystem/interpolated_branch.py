"""
interpolated_branch.py
"""

from flatland.connector_subsystem.branch import Branch
from flatland.datatypes.connection_types import NodeFace, Orientation
from typing import Set, TYPE_CHECKING
from flatland.flatland_exceptions import BranchCannotBeInterpolated
from flatland.connector_subsystem.anchored_tree_stem import AnchoredTreeStem
from flatland.datatypes.general_types import Index

if TYPE_CHECKING:
    from flatland.connector_subsystem.tree_connector import TreeConnector


class InterpolatedBranch(Branch):
    def __init__(self, order: Index, connector: 'TreeConnector', hanging_stems: Set[AnchoredTreeStem]):
        """
        If the user does not specify any positional information for a Branch, its position
        is interpolated at the midpoint between the opposing Node faces of the hanging
        stems. If the opposing node faces are top/bottom, the axis will be horizontal,
        otherwise vertical.

        If there are no opposing faces (all faces on the same side), the branch will be drawn
        as close as possible to the face furthest in the attached node face direction.
        Furthest right(right face), furthest left(left face), furthest down(bottom face),
        furthest up(top face).

        :param order: Ordinal value used as index into the Tree Connector branch sequence
        :param connector: The Tree Connector
        :param hanging_stems: A set of Anchored Tree Stems hanging on the Rut Branch
        """
        # The axis of this branch is either an x or y canvas coordinate value
        # An Interpolated Branch is always drawn between sets of opposing stems
        # The stems either rise and descend vertically to meet on a horizontal axis
        # or extend rightward and leftward to meet on a vertical axis

        # If an interpolated branch was specified by the user but there are no opposing stems/faces
        # there is a user error

        # Compute the branch axis and orientation so we can init the superclass

        # All node faces for downward or leftward stems will have the highest y or x values
        # The opposing faces will then have the lowest y or x values
        # We then take the middle point between the lowest high value and the highest of the low values
        # By adding this to the highest low value we get the canvas coordinate of the branch axis

        # TODO: Handle no opposition (faces all on same side interpolation case)

        downward_stems = {s for s in hanging_stems if s.Node_face == NodeFace.BOTTOM}
        axis_orientation = Orientation.Horizontal if downward_stems else Orientation.Vertical
        high_stems = downward_stems if downward_stems else {s for s in hanging_stems if s.Node_face == NodeFace.LEFT}
        low_stems = hanging_stems - high_stems
        if not (low_stems and high_stems):
            raise BranchCannotBeInterpolated
        lowest_high_face = min({s.Node.Face_position(s.Node_face) for s in high_stems})
        highest_low_face = max({s.Node.Face_position(s.Node_face) for s in low_stems})
        assert highest_low_face < lowest_high_face
        axis = highest_low_face + (lowest_high_face - highest_low_face) / 2
        Branch.__init__(self, order, axis, connector, hanging_stems, axis_orientation)
