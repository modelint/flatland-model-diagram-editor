"""
xuml_statemachine_diagram.py – Generates a state machine diagram for an xuml model using the Flatland draw engine
"""

import sys
import logging
from pathlib import Path
from flatland.flatland_exceptions import FlatlandIOException, MultipleFloatsInSameBranch
from flatland.flatland_exceptions import LayoutParseError, ModelParseError
from flatland.input.statemodel_parser import StateModelParser
from flatland.input.layout_parser import LayoutParser
from flatland.database.flatlanddb import FlatlandDB
from flatland.node_subsystem.canvas import Canvas
from flatland.sheet_subsystem.frame import Frame
from flatland.node_subsystem.single_cell_node import SingleCellNode
from flatland.node_subsystem.spanning_node import SpanningNode
from flatland.datatypes.geometry_types import Alignment, VertAlign, HorizAlign
from flatland.datatypes.command_interface import New_Stem, New_Path
from typing import Optional, Dict
from collections import namedtuple
from flatland.connector_subsystem.straight_binary_connector import StraightBinaryConnector
from flatland.connector_subsystem.bending_binary_connector import BendingBinaryConnector
from flatland.datatypes.connection_types import ConnectorName, OppositeFace, StemName
from flatland.text.text_block import TextBlock

class XumlStateMachineDiagram:

    def __init__(self, xuml_model_path: Path, flatland_layout_path: Path, diagram_file_path: Path,
                 rebuild: bool, show_grid: bool, nodes_only: bool):
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
            self.model = StateModelParser(model_file_path=self.xuml_model_path, debug=False)
        except FlatlandIOException as e:
            sys.exit(e)
        try:
            self.statemodel = self.model.parse()
        except ModelParseError as e:
            sys.exit(e)

        self.logger.info("Parsing the layout")
        # Parse the layout
        try:
            self.layout = LayoutParser(layout_file_path=self.flatland_layout_path, debug=False)
        except FlatlandIOException as e:
            sys.exit(e)
        try:
            self.layout = self.layout.parse()
        except LayoutParseError as e:
            sys.exit(e)

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
                canvas=self.flatland_canvas, metadata=self.statemodel.metadata
            )

        # Draw all of the states
        self.logger.info("Drawing the states")
        self.nodes = self.draw_states()

        # # If there are any relationships, draw them
        # if self.subsys.rels and not nodes_only:
        #     cp = self.layout.connector_placement
        #     for r in self.subsys.rels:  # r is the model data without any layout info
        #         rnum = r['rnum']
        #         rlayout = cp.get(rnum)  # How this r is to be laid out on the diagram
        #         if not rlayout:
        #             self.logger.warning(f"Relationship {rnum} skipped, no placement in layout sheet.")
        #             continue
        #
        #         if 'superclass' in r.keys():
        #             self.draw_generalization(rnum=rnum, generalization=r, tree_layout=rlayout)
        #         else:
        #             self.draw_association(rnum=rnum, association=r, binary_layout=rlayout)
        #
        #     # Check to see if any connector placements were specified for non-existent relationships
        #     rnum_placements = {r for r in cp.keys()}
        #     rnum_defs = {r['rnum'] for r in self.subsys.rels}
        #     orphaned_placements = rnum_placements - rnum_defs
        #     if orphaned_placements:
        #         self.logger.warning(f"Connector placements {orphaned_placements} in layout sheet refer to undeclared relationships")

        self.logger.info("Rendering the Canvas")
        self.flatland_canvas.render()

    def create_canvas(self) -> Canvas:
        """Create a blank canvas"""
        lspec = self.layout.layout_spec
        return Canvas(
            diagram_type=lspec.dtype,
            presentation=lspec.pres,
            notation=lspec.notation,
            standard_sheet_name=lspec.sheet,
            orientation=lspec.orientation,
            diagram_padding=lspec.padding,
            drawoutput=self.diagram_file_path,
            show_grid=self.show_grid,
        )

    def draw_states(self) -> Dict[str, SingleCellNode]:
        """Draw all of the states on the state machine diagram"""

        nodes = {}
        np = self.layout.node_placement # Layout data for all classes

        for state in self.statemodel.states:

            # Get the state name from the model
            self.logger.info(f'Processing state: {state.name}')

            # Get the layout data for this state
            nlayout = np.get(state.name)
            if not nlayout:
                self.logger.warning(f"Skipping state [{state.name}] -- No placement specified in layout sheet")
                continue

            # Layout data for all placements
            # By default the class name is all on one line, but it may be wrapped across multiple
            nlayout['wrap'] = nlayout.get('wrap', 1)
            # There is an optional keyletter (class name abbreviation) displayed as {keyletter}
            # after the class name
            name_block = TextBlock(state.name, nlayout['wrap'])
            # Now assemble all the text content for each class compartment
            # One list item per compartment in descending vertical order of display
            # (class name, attributes and optional methods)
            text_content = [name_block.text, state.activity ]

            for i, p in enumerate(nlayout['placements']):
                h = HorizAlign[p.get('halign', 'CENTER')]
                v = VertAlign[p.get('valign', 'CENTER')]
                expansion_percent = max(min(100, nlayout.get('node_expansion', 0)), 1)
                expansion_ratio = round(expansion_percent / 100, 2)
                # If this is an imported class, append the import reference to the attribute list
                row_span, col_span = p['node_loc']
                # If methods were supplied, include them in content
                # text content includes text for all compartments other than the title compartment
                # When drawing connectors, we want to attach to a specific node placement
                # In most cases, this will just be the one and only indicated by the node name
                # But if a node is duplicated, i will not be 0 and we add a suffix to the node
                # name for the additional placement
                node_name = state.name if i == 0 else f'{state.name}_{i+1}'
                if len(row_span) == 1 and len(col_span) == 1:
                    nodes[node_name] = SingleCellNode(
                        node_type_name='state',
                        content=text_content,
                        grid=self.flatland_canvas.Diagram.Grid,
                        row=row_span[0], column=col_span[0],
                        local_alignment=Alignment(vertical=v, horizontal=h),
                        expansion=expansion_ratio
                    )
                else:
                    # Span might be only 1 column or row
                    low_row = row_span[0]
                    high_row = low_row if len(row_span) == 1 else row_span[1]
                    left_col = col_span[0]
                    right_col = left_col if len(col_span) == 1 else col_span[1]
                    nodes[node_name] = SpanningNode(
                        node_type_name='state',
                        content=text_content,
                        grid=self.flatland_canvas.Diagram.Grid,
                        low_row=low_row, high_row=high_row,
                        left_column=left_col, right_column=right_col,
                        local_alignment=Alignment(vertical=v, horizontal=h),
                        expansion=expansion_ratio
                    )
        return nodes

    # def draw_association(self, rnum, association, binary_layout):
    #     """Draw the binary association"""
    #     # Straight or bent connector?
    #     tstem = binary_layout['tstem']
    #     pstem = binary_layout['pstem']
    #     reversed = False  # Assume that layout sheet and model order matches
    #     astem = binary_layout.get('tertiary_node', None)
    #
    #     t_side = association['t_side']
    #     if tstem['node_ref'][0] != t_side['cname']:
    #         # The user put the tstems in the wrong order in the layout file
    #         # Swap them
    #         # The node_ref is a list and the first element refers to the model class name
    #         # (the 2nd element indicates duplicate placement, if any, and is not relevant for the comparison above)
    #         tstem, pstem = pstem, tstem
    #         reversed = True
    #         self.logger.info(f"Stems order in layout file does not match model, swapping stem order for connector {rnum}")
    #
    #     t_phrase = StemName(
    #         text=TextBlock(t_side['phrase'], wrap=tstem['wrap']),
    #         side=tstem['stem_dir'], axis_offset=None, end_offset=None
    #     )
    #     node_ref = make_node_ref(tstem['node_ref'])
    #     t_stem = New_Stem(stem_type='class mult', semantic=t_side['mult'] + ' mult',
    #                       node=self.nodes[node_ref], face=tstem['face'],
    #                       anchor=tstem.get('anchor', None), stem_name=t_phrase)
    #
    #     # Same as for the t_side, but with p instead
    #     p_side = association['p_side']
    #     p_phrase = StemName(
    #         text=TextBlock(p_side['phrase'], wrap=pstem['wrap']),
    #         side=pstem['stem_dir'], axis_offset=None, end_offset=None
    #     )
    #     node_ref = make_node_ref(pstem['node_ref'])
    #     try:
    #         pnode = self.nodes[node_ref]
    #     except KeyError:
    #         missing_side = "p-stem" if not reversed else "t-stem"
    #         self.logger.error(f"In layout sheet {missing_side} of {rnum} class [{node_ref}] is not defined in model")
    #         sys.exit()
    #     p_stem = New_Stem(stem_type='class mult', semantic=p_side['mult'] + ' mult',
    #                       node=pnode, face=pstem['face'],
    #                       anchor=pstem.get('anchor', None), stem_name=p_phrase)
    #     # There is an optional stem for an association class
    #     if astem:
    #         node_ref = make_node_ref(astem['node_ref'])
    #         try:
    #             semantic = association['assoc_mult'] + ' mult'
    #         except KeyError:
    #             self.logger.error(
    #                 f"Layout sheet calls for ternary stem, but class model does not specify any"
    #                 f" association class on association: {rnum}")
    #             sys.exit()
    #         try:
    #             node=self.nodes[node_ref]
    #         except KeyError:
    #             self.logger.error(
    #                 f"Association class [{node_ref}] is missing in relationship {rnum}"
    #             )
    #             sys.exit()
    #         a_stem = New_Stem(stem_type='associative mult', semantic=semantic,
    #                           node=self.nodes[node_ref], face=astem['face'], anchor=astem.get('anchor', None),
    #                           stem_name=None)
    #     else:
    #         a_stem = None
    #     rnum_data = ConnectorName(text=rnum, side=binary_layout['dir'], bend=binary_layout['bend'])
    #
    #     paths = None if not binary_layout.get('paths', None) else \
    #         [New_Path(lane=p['lane'], rut=p['rut']) for p in binary_layout['paths']]
    #
    #     if not paths and OppositeFace[tstem['face']] == pstem['face']:
    #         StraightBinaryConnector(
    #             diagram=self.flatland_canvas.Diagram,
    #             connector_type='binary association',
    #             t_stem=t_stem,
    #             p_stem=p_stem,
    #             tertiary_stem=a_stem,
    #             name=rnum_data
    #         )
    #     else:
    #         BendingBinaryConnector(
    #             diagram=self.flatland_canvas.Diagram,
    #             connector_type='binary association',
    #             anchored_stem_p=p_stem,
    #             anchored_stem_t=t_stem,
    #             tertiary_stem=a_stem,
    #             paths=paths,
    #             name=rnum_data)