"""
xUML_class_diagram.py – Generates an xuml diagram for an xuml model using the Flatland draw engine
"""

import sys
import logging
from pathlib import Path
from flatland.flatland_exceptions import FlatlandIOException, MultipleFloatsInSameBranch
from flatland.input.model_parser import ModelParser
from flatland.input.layout_parser import LayoutParser
from flatland.database.flatlanddb import FlatlandDB
from flatland.node_subsystem.canvas import Canvas
from flatland.sheet_subsystem.frame import Frame
from flatland.node_subsystem.single_cell_node import SingleCellNode
from flatland.node_subsystem.spanning_node import SpanningNode
from flatland.connector_subsystem.tree_connector import TreeConnector
from flatland.datatypes.geometry_types import Alignment, VertAlign, HorizAlign, Padding
from flatland.datatypes.command_interface import New_Stem, New_Path, New_Trunk_Branch, New_Offshoot_Branch, New_Branch_Set
from typing import Optional, Dict
from collections import namedtuple
from flatland.connector_subsystem.straight_binary_connector import StraightBinaryConnector
from flatland.connector_subsystem.bending_binary_connector import BendingBinaryConnector
from flatland.datatypes.connection_types import ConnectorName, OppositeFace, StemName
from flatland.text.text_block import TextBlock

BranchLeaves = namedtuple('BranchLeaves', 'leaf_stems local_graft next_graft floating_leaf_stem')

def make_node_ref(node_ref) -> str:
    """
    Composes a fully qualified placement name based on a node reference in a layout file

    :param node_ref:  A layout reference to a node placement
    :return: The model elment name if it is only placed once, otherwise name suffixed by an underscore and a numbered placement
    """
    return node_ref[0] if len(node_ref) < 2 else f"{node_ref[0]}_{node_ref[1]}"

class XumlClassDiagram:

    def __init__(self, xuml_model_path: Path, flatland_layout_path: Path, diagram_file_path: Path,
                 rebuild: bool, show_grid: bool):
        """Constructor"""
        self.logger = logging.getLogger(__name__)
        self.xuml_model_path = xuml_model_path
        self.flatland_layout_path = flatland_layout_path
        self.diagram_file_path = diagram_file_path
        self.rebuild = rebuild
        self.show_grid = show_grid

        self.logger.info("Parsing the model")
        # Parse the model
        try:
            self.model = ModelParser(model_file_path=self.xuml_model_path, debug=False)
        except FlatlandIOException as e:
            sys.exit(e)
        self.subsys = self.model.parse()

        self.logger.info("Parsing the layout")
        # Parse the layout
        try:
            self.layout = LayoutParser(layout_file_path=self.flatland_layout_path, debug=False)
        except FlatlandIOException as e:
            sys.exit(e)
        self.layout = self.layout.parse()

        # Load the flatland database
        self.db = FlatlandDB(rebuild=self.rebuild)
        if self.rebuild:
            from flatland.sheet_subsystem.titleblock_placement import TitleBlockPlacement
            TitleBlockPlacement()

        # Draw the blank canvas of the appropriate size, diagram type and presentation style
        self.logger.info("Creating the canvas")
        self.flatland_canvas = self.create_canvas()

        # Draw the frame and title block if one was supplied
        if self.layout.layout_spec.frame:
            self.logger.info("Creating the frame")
            self.frame = Frame(
                name=self.layout.layout_spec.frame, presentation=self.layout.layout_spec.frame_presentation,
                canvas=self.flatland_canvas, metadata=self.subsys.metadata
            )

        # Draw all of the classes
        self.logger.info("Drawing the classes")
        self.nodes = self.draw_classes()

        # If there are any relationships, draw them
        if self.subsys.rels:
            cp = self.layout.connector_placement
            for r in self.subsys.rels:  # r is the model data without any layout info
                rnum = r['rnum']
                rlayout = cp[rnum]  # How this r is to be laid out on the diagram
                if 'superclass' in r.keys():
                    self.draw_generalization(rnum=rnum, generalization=r, tree_layout=rlayout)
                else:
                    self.draw_association(rnum=rnum, association=r, binary_layout=rlayout)

        self.logger.info("Rendering the Canvas")
        self.flatland_canvas.render()

    def create_canvas(self) -> Canvas:
        """Create a blank canvas"""
        lspec = self.layout.layout_spec
        if not lspec.padding:
            pad_l, pad_b, pad_t, pad_r = 0, 0, 0, 0
        else:
            pad_l, pad_b, pad_t, pad_r = lspec.padding.values()
        padding = Padding(top=pad_t, bottom=pad_b, left=pad_l, right=pad_r)
        return Canvas(
            diagram_type=lspec.dtype,
            presentation=lspec.pres,
            notation=lspec.notation,
            standard_sheet_name=lspec.sheet,
            orientation=lspec.orientation,
            diagram_padding=padding,
            drawoutput=self.diagram_file_path,
            show_grid=self.show_grid,
        )

    def draw_classes(self) -> Dict[str, SingleCellNode]:
        """Draw all of the classes on the class diagram"""

        nodes = {}
        np = self.layout.node_placement # Layout data for all classes

        for c in self.subsys.classes:

            # Get the class name from the model
            cname = c['name']
            self.logger.info(f'Processing class: {cname}')

            # Get the layout data for this class
            nlayout = np[cname]

            # Layout data for all placements
            # By default the class name is all on one line, but it may be wrapped across multiple
            nlayout['wrap'] = nlayout.get('wrap', 1)
            # There is an optional keyletter (class name abbreviation) displayed as {keyletter}
            # after the class name
            keyletter = c.get('keyletter')
            keyletter_display = f' {{{keyletter}}}' if keyletter else ''
            # Class name and optional keyletter are in the same wrapped text block
            name_block = TextBlock(cname+keyletter_display, nlayout['wrap'])
            # Class might be imported. If so add a reference to subsystem or TBD in attr compartment
            import_subsys_name = c.get('import')
            if not import_subsys_name:
                internal_ref = []
            elif import_subsys_name.endswith('TBD'):
                internal_ref = [' ', f'{import_subsys_name.removesuffix(" TBD")} subsystem', '(not yet modeled)']
            else:
                internal_ref = [' ', f'(See {import_subsys_name} subsystem)']
            # Now assemble all the text content for each class compartment
            # One list item per compartment in descending vertical order of display
            # (class name, attributes and optional methods)
            text_content = [name_block.text, c['attributes'] + internal_ref ]
            if c.get('methods'):
                text_content.append(c['methods'])

            # The same class may be placed more than once so that the connectors
            # have less bends and crossovers. This is usually, but not limited to,
            # the placement of imported classes. Since we generate the diagram
            # from a single model, there is no harm in duplicating the same class on a
            # diagram.

            for i, p in enumerate(nlayout['placements']):
                h = HorizAlign[p.get('halign', 'CENTER')]
                v = VertAlign[p.get('valign', 'CENTER')]
                # If this is an imported class, append the import reference to the attribute list
                row_span, col_span = p['node_loc']
                # If methods were supplied, include them in content
                # text content includes text for all compartments other than the title compartment
                # When drawing connectors, we want to attach to a specific node placement
                # In most cases, this will just be the one and only indicated by the node name
                # But if a node is duplicated, i will not be 0 and we add a suffix to the node
                # name for the additional placement
                node_name = cname if i == 0 else f'{cname}_{i+1}'
                if len(row_span) == 1 and len(col_span) == 1:
                    nodes[node_name] = SingleCellNode(
                        node_type_name='class' if not import_subsys_name else 'imported class',
                        content=text_content,
                        grid=self.flatland_canvas.Diagram.Grid,
                        row=row_span[0], column=col_span[0],
                        local_alignment=Alignment(vertical=v, horizontal=h)
                    )
                else:
                    # Span might be only 1 column or row
                    low_row = row_span[0]
                    high_row = low_row if len(row_span) == 1 else row_span[1]
                    left_col = col_span[0]
                    right_col = left_col if len(col_span) == 1 else col_span[1]
                    nodes[node_name] = SpanningNode(
                        node_type_name='class' if not import_subsys_name else 'imported class',
                        content=text_content,
                        grid=self.flatland_canvas.Diagram.Grid,
                        low_row=low_row, high_row=high_row,
                        left_column=left_col, right_column=right_col,
                        local_alignment=Alignment(vertical=v, horizontal=h)
                    )
        return nodes
        # TODO:  Add support for axis offset on stem names

    def draw_association(self, rnum, association, binary_layout):
        """Draw the binary association"""
        # Straight or bent connector?
        tstem = binary_layout['tstem']
        pstem = binary_layout['pstem']
        astem = binary_layout.get('tertiary_node', None)

        t_side = association['t_side']
        if tstem['node_ref'][0] != t_side['cname']:
            # The user put the tstems in the wrong order in the layout file
            # Swap them
            # The node_ref is a list and the first element refers to the model class name
            # (the 2nd element indicates duplicate placement, if any, and is not relevant for the comparison above)
            tstem, pstem = pstem, tstem
            self.logger.warning(f"Stems order in layout file does not match model, swapping stem order for connector {rnum}")

        t_phrase = StemName(
            text=TextBlock(t_side['phrase'], wrap=tstem['wrap']),
            side=tstem['stem_dir'], axis_offset=None, end_offset=None
        )
        node_ref = make_node_ref(tstem['node_ref'])
        t_stem = New_Stem(stem_type='class mult', semantic=t_side['mult'] + ' mult',
                          node=self.nodes[node_ref], face=tstem['face'],
                          anchor=tstem.get('anchor', None), stem_name=t_phrase)

        # Same as for the t_side, but with p instead
        p_side = association['p_side']
        p_phrase = StemName(
            text=TextBlock(p_side['phrase'], wrap=pstem['wrap']),
            side=pstem['stem_dir'], axis_offset=None, end_offset=None
        )
        node_ref = make_node_ref(pstem['node_ref'])
        p_stem = New_Stem(stem_type='class mult', semantic=p_side['mult'] + ' mult',
                          node=self.nodes[node_ref], face=pstem['face'],
                          anchor=pstem.get('anchor', None), stem_name=p_phrase)
        # There is an optional stem for an association class
        if astem:
            node_ref = make_node_ref(astem['node_ref'])
            a_stem = New_Stem(stem_type='associative mult', semantic=association['assoc_mult'] + ' mult',
                              node=self.nodes[node_ref], face=astem['face'], anchor=astem.get('anchor', None),
                              stem_name=None)
        else:
            a_stem = None
        rnum_data = ConnectorName(text=rnum, side=binary_layout['dir'], bend=binary_layout['bend'])

        paths = None if not binary_layout.get('paths', None) else \
            [New_Path(lane=p['lane'], rut=p['rut']) for p in binary_layout['paths']]

        if not paths and OppositeFace[tstem['face']] == pstem['face']:
            StraightBinaryConnector(
                diagram=self.flatland_canvas.Diagram,
                connector_type='binary association',
                t_stem=t_stem,
                p_stem=p_stem,
                tertiary_stem=a_stem,
                name=rnum_data
            )
        else:
            BendingBinaryConnector(
                diagram=self.flatland_canvas.Diagram,
                connector_type='binary association',
                anchored_stem_p=p_stem,
                anchored_stem_t=t_stem,
                tertiary_stem=a_stem,
                paths=paths,
                name=rnum_data)

    def process_leaf_stems(self, lfaces, preceeding_graft: Optional[New_Stem]) -> BranchLeaves:
        """

        :param lfaces:
        :param preceeding_graft: The trunk stem if this is a trunk branch or some leaf stem from the preceeding branch
        :return: branch_leaves
        """
        # A local graft is a stem that establishes the axis of our branch from which all the nodes hang
        # A next branch graft is a stem that establishes that axis for the succeeding branch
        # A floating leaf stem is one that aligns itself with the branch axis (rather than hanging from it)
        # See the tech note tn.2 in the documentation for helpful illustrations of all this

        leaf_stems = set()  # The set of leaf stems that we will create and return
        next_branch_graft = None  # We'll look for at most one of these
        floating_leaf_stem = None  # And at most one of these
        graft = preceeding_graft  # If supplied, we have our one and only local graft

        for name in lfaces.keys():

            anchor = lfaces[name]['anchor']  # Assume that this is not a floating stem
            if lfaces[name]['anchor'] == 'float':
                if floating_leaf_stem:
                    # At most one floating leaf stem permitted in a branch
                    # The parser should have caught this error, but just in case
                    raise MultipleFloatsInSameBranch(set(lfaces.keys()))
                anchor = None

            # Current leaf stem
            lstem = New_Stem(stem_type='subclass', semantic='subclass', node=self.nodes[name],
                             face=lfaces[name]['face'], anchor=anchor, stem_name=None)
            leaf_stems.add(lstem)

            if lfaces[name]['anchor'] == 'float':
                floating_leaf_stem = lstem  # Set the one and only anchorless stem for this branch

            # Graft status
            # If no graft has been set (trunk stem or leaf in preceeding branch as next_branch_graft)
            if not graft and lfaces[name]['graft'] == 'local':
                # A branch can have at most one graft
                graft = lstem

            # Check next branch graft status of this leaf stem
            if not next_branch_graft and lfaces[name]['graft'] == 'next':
                # There can only be one in a branch and the parser should ensure this, raising errors on duplicates
                # Remember the first next branch found, if any
                # We'll use it to graft the subsequent offshoot branch
                next_branch_graft = lstem

        return BranchLeaves(leaf_stems=leaf_stems, local_graft=graft, next_graft=next_branch_graft,
                            floating_leaf_stem=floating_leaf_stem)

    def draw_generalization(self, rnum, generalization, tree_layout):
        """
        One of the rare times it is a good idea to draw one – LS
        """
        trunk_layout = tree_layout['trunk_face']
        node_ref = make_node_ref(trunk_layout['node_ref'])
        trunk_node = self.nodes[node_ref]

        # Process trunk branch
        trunk_stem = New_Stem(stem_type='superclass', semantic='superclass', node=trunk_node,
                              face=trunk_layout['face'], anchor=trunk_layout['anchor'], stem_name=None)
        tbranch = tree_layout['branches'][0]  # First branch is required and it is the trunk branch
        path_fields = tbranch.get('path', None)
        tbranch_path = None if not path_fields else New_Path(**path_fields)
        leaves = self.process_leaf_stems(
            lfaces=tbranch['leaf_faces'],
            preceeding_graft=trunk_stem if trunk_layout['graft'] else None
        )
        next_branch_graft = leaves.next_graft  # Has a value if some leaf is the graft for the next offshoot branch

        # Create the trunk branch with all of its leaf stems
        trunk_branch = New_Trunk_Branch(
            trunk_stem=trunk_stem, leaf_stems=leaves.leaf_stems, graft=leaves.local_graft,
            path=tbranch_path, floating_leaf_stem=leaves.floating_leaf_stem
        )

        # Process any other offshoot branches (branches other than the trunk branch)
        obranches = []  # Sequence of offshoot branches (usually ends up empty or with only one or two offshoots)
        for obranch in tree_layout['branches'][1:]:
            path_fields = obranch.get('path', None)
            obranch_path = None if not path_fields else New_Path(**path_fields)
            leaves = self.process_leaf_stems(
                lfaces=obranch['leaf_faces'],
                preceeding_graft=next_branch_graft
            )
            obranches.append(
                New_Offshoot_Branch(leaf_stems=leaves.leaf_stems, graft=leaves.local_graft, path=obranch_path,
                                    floating_leaf_stem=leaves.floating_leaf_stem)
            )

        # Now draw the generalization
        branches = New_Branch_Set(trunk_branch=trunk_branch, offshoot_branches=obranches)
        rnum_data = ConnectorName(text=rnum, side=tree_layout['dir'], bend=None)
        TreeConnector(diagram=self.flatland_canvas.Diagram, connector_type='generalization',
                      branches=branches, name=rnum_data)
