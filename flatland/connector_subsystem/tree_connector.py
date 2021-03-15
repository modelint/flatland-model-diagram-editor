"""
tree_connector.py
"""
from flatland.flatland_exceptions import UnsupportedConnectorType
from flatland.datatypes.connection_types import ConnectorName
from flatland.connector_subsystem.connector import Connector
from flatland.connector_subsystem.trunk_stem import TrunkStem
from flatland.connector_subsystem.grafted_branch import GraftedBranch
from flatland.connector_subsystem.interpolated_branch import InterpolatedBranch
from flatland.connector_subsystem.rut_branch import RutBranch
from flatland.datatypes.geometry_types import Position
from flatland.datatypes.command_interface import New_Branch_Set, New_Stem
from flatland.connector_subsystem.anchored_leaf_stem import AnchoredLeafStem
from flatland.node_subsystem.diagram import Diagram
from collections import namedtuple
from typing import Set, Optional
from flatland.datatypes.general_types import Index

StemGroup = namedtuple('StemGroup', 'hanging_stems grafting_stem new_floating_stem, path')
"""
"""
LeafGroup = namedtuple('LeafGroup', 'hleaves gleaf')
"""
A set of Anchored Stems where one may be designated as a grafting leaf, see class model R157

    Attributes
    
    - hleaves -- Anchored Tree Stems which are hanging leaves
    - gleaf -- An optional Anchored Tree Stem that grafts an offshoot Branch
"""


class TreeConnector(Connector):
    """
    A Tree Connector connects a trunk Node to one or more branch Nodes in a tree structure. It can be used to
    draw a generalization relationship on a class diagram, for example.

        Attributes

        - Trunk_stem -- This Stem attaches the single Node in the trunk position
        - Leaf_stems -- The Branch Stems organized as a sequence of sets. Each set connects to the same line segment.
    """

    def __init__(self, diagram: Diagram, connector_type: str, branches: New_Branch_Set,
                 name: Optional[ConnectorName] = None):
        """
        Constructor

        :param diagram: Reference to Diagram
        :param connector_type: Name of Connector Type
        :param branches:
        :param name: An name (optional depending on the Connector Type) for the Connector
        """
        # Verify that the specified connector type name corresponds to a supported connector type
        # found in our database
        try:
            ct = diagram.Diagram_type.ConnectorTypes[connector_type]
        except IndexError:
            raise UnsupportedConnectorType(
                connector_type_name=connector_type, diagram_type_name=diagram.Diagram_type.Name)
        Connector.__init__(self, diagram=diagram, connector_type=ct, name=name)

        # Unpack new trunk spec and create its Anchored Trunk Stem
        new_tstem = branches.trunk_branch.trunk_stem  # Get the Trunk New Stem user specification
        self.Trunk_stem = self.unpack_trunk(new_tstem)  # Unpack the user specification into Trunk Stem object
        # If the trunk stem has been specified as a grafting stem, make it this branch's gstem
        gstem = self.Trunk_stem if branches.trunk_branch.graft == new_tstem else None

        # Unpack the leaf stems for the trunk branch (there must be at least one leaf)
        assert len(branches.trunk_branch.leaf_stems) > 0, "No leaf stems specified for trunk branch"
        unpacked_hanging_stems = self.unpack_hanging_leaves(
            new_leaves=branches.trunk_branch.leaf_stems,
            new_graft_leaf=branches.trunk_branch.graft
        )
        self.Leaf_stems = unpacked_hanging_stems.hleaves  # Anchored Leaf Stems that do not graft any Branch
        assert not (gstem and unpacked_hanging_stems.gleaf), "Both trunk and a leaf stem grafts in the same branch"
        # gstem is an optional Anchored Leaf Stem that grafts an offshoot branch
        gstem = unpacked_hanging_stems.gleaf if unpacked_hanging_stems.gleaf else None

        # Create a set of all AnchoredTreeStem objects in the Trunk Branch, including the Trunk Stem
        anchored_tree_stems = {s for s in self.Leaf_stems}
        anchored_tree_stems.add(self.Trunk_stem)

        trunk_branch_stem_group = StemGroup(
            hanging_stems=anchored_tree_stems,  # Anchored Tree Stem objects
            grafting_stem=gstem,  # Anchored Tree Stem object
            new_floating_stem=branches.trunk_branch.floating_leaf_stem,  # Still a New Stem user specification
            path=branches.trunk_branch.path  # Optional Path (named tuple) where the branch is drawn
        )
        branches_to_make = [trunk_branch_stem_group]  # first branch in the sequence
        # We will iterate through these further down and, for each,
        # create the appropriate branch type

        # Now go through any offshoot branches to complete the branches_to_make sequence

        for o in branches.offshoot_branches:
            unpacked_hanging_stems = self.unpack_hanging_leaves(o.leaf_stems, o.graft)
            self.Leaf_stems = self.Leaf_stems.union(unpacked_hanging_stems.hleaves)
            trunk_branch_stem_group = StemGroup(
                hanging_stems=unpacked_hanging_stems.hleaves,
                grafting_stem=unpacked_hanging_stems.gleaf,
                new_floating_stem=o.floating_leaf_stem,
                path=o.path
            )
            branches_to_make.append(trunk_branch_stem_group)

        # Create all of the branches
        assert len(branches_to_make) > 0, "No branches to make"

        self.Branches = []
        for i, b in enumerate(branches_to_make):
            order = Index(i)  # Cast INT to Index type
            if b.path:
                this_branch = RutBranch(order=order, connector=self, path=b.path, hanging_stems=b.hanging_stems)
            elif b.grafting_stem:
                this_branch = GraftedBranch(order=order, connector=self, hanging_stems=b.hanging_stems,
                                            grafting_stem=b.grafting_stem, new_floating_stem=b.new_floating_stem)
            else:
                this_branch = InterpolatedBranch(order, connector=self, hanging_stems=b.hanging_stems)
            self.Branches.append(this_branch)

    def unpack_hanging_leaves(self, new_leaves: Set[New_Stem], new_graft_leaf: Optional[New_Stem]) -> LeafGroup:
        """
        Unpack all new anchored leaves for a branch
        :param new_leaves:  A set of new leaf specifications provided by the user
        :param new_graft_leaf: The optional user designated grafting leaf stem for the Branch
        :return: The newly created AnchoredLeafStem objects and an optional reference to one that grafts an
                 offshoot branch
        """
        hanging_leaves = set()  # Of AnchoredLeafStem objects
        hanging_graft_leaf = None
        # Create Leaf Stems
        for leaf_stem in new_leaves:
            # Lookup the StemType object
            leaf_stem_type = self.Connector_type.Stem_type[leaf_stem.stem_type]
            if leaf_stem.anchor is not None:
                anchored_hanging_leaf = AnchoredLeafStem(
                    connector=self,
                    stem_type=leaf_stem_type,
                    semantic=leaf_stem.semantic,
                    node=leaf_stem.node,
                    face=leaf_stem.face,
                    anchor_position=leaf_stem.anchor
                )
                hanging_leaves.add(anchored_hanging_leaf)
                # Check to see if this is a grafting stem, if so register this newly created leaf as such
                if not hanging_graft_leaf and leaf_stem == new_graft_leaf:
                    # There can only be one, so do this assignment at most once per new_leaves set
                    hanging_graft_leaf = anchored_hanging_leaf
        return LeafGroup(hleaves=hanging_leaves, gleaf=hanging_graft_leaf)

    def unpack_trunk(self, new_trunk: New_Stem) -> TrunkStem:
        """
        Unpack the trunk New Stem user specification for this Tree Connector

        :param new_trunk: (New_Stem) user specification of a Stem
        :return: (TrunkStem) object, which is ultimately a subclass of Anchored Stem
        """
        return TrunkStem(
            connector=self,  # Connector object (our Tree Connector)
            stem_type=self.Connector_type.Stem_type[new_trunk.stem_type],  # StemType object loaded from db
            semantic=new_trunk.semantic,  # str
            node=new_trunk.node,  # Node object
            face=new_trunk.face,  # NodeFace
            anchor_position=new_trunk.anchor  # AnchorPosition (int)
        )

    def render(self):
        """
        Draw the Branch line segment for a single-branch Tree Connector
        """
        layer = self.Diagram.Layer
        for b in self.Branches:
            b.render()
        self.Trunk_stem.render()

        # Draw the connector name if any
        name_spec = self.Connector_type.Name_spec
        vbuffer, hbuffer = name_spec.axis_buffer
        root_end = self.Trunk_stem.Root_end
        vine_end = self.Trunk_stem.Vine_end
        if root_end.x == vine_end.x:
            # Vertical stem
            # If the lower left corner of the name is below the vine end (bottom face)
            # we will need to subtract the height of the bounding box
            if root_end.y > vine_end.y:
                name_y = vine_end.y - self.Name_size.height  # Shift name below the node face
            else:
                name_y = vine_end.y # Shift name above the node face
            if self.Name.side == 1:  # User trunk stem side preference
                name_x = vine_end.x + hbuffer  # Shift name to the right
            else:
                name_x = vine_end.x - (hbuffer + self.Name_size.width)  # Shift name to the left
        else:
            # Horizontal stem
            if root_end.x > vine_end.x:
                name_x = vine_end.x - self.Name_size.width  # Shift name left of the node face
            else:
                name_x = vine_end.x  # Shift name right of the node face
            if self.Name.side == 1:  # User trunk stem side preference
                name_y = vine_end.y + vbuffer  # Shift name above the stem
            else:
                name_y = vine_end.y - (vbuffer + self.Name_size.height)  # Shift name below the stem

        name_position = Position(name_x, name_y)
        layer.add_text_line(
            asset=self.Connector_type.Name + ' name',
            lower_left=name_position, text=self.Name.text, underlay_asset='name underlay')
