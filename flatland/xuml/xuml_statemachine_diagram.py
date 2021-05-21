"""
xuml_statemachine_diagram.py – Generates a state machine diagram for an xuml model using the Flatland draw engine
"""

import sys
import logging
from pathlib import Path
from flatland.flatland_exceptions import FlatlandIOException
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
from typing import Dict
from flatland.connector_subsystem.unary_connector import UnaryConnector
from flatland.connector_subsystem.straight_binary_connector import StraightBinaryConnector
from flatland.connector_subsystem.bending_binary_connector import BendingBinaryConnector
from flatland.datatypes.connection_types import ConnectorName, OppositeFace
from flatland.text.text_block import TextBlock


def make_event_cname(ev_spec) -> str:
    """Create a transition connector name based on an event name and an optional signature"""
    if not ev_spec.signature:
        return ev_spec.name
    else:
        return ev_spec.name + '( ' + ', '.join( [f'{p.name}:{p.type}' for p in ev_spec.signature]) + ' )'


class XumlStateMachineDiagram:

    def __init__(self, xuml_model_path: Path, flatland_layout_path: Path, diagram_file_path: Path,
                 rebuild: bool, show_grid: bool, nodes_only: bool, no_color: bool):
        """Constructor"""
        self.logger = logging.getLogger(__name__)
        self.xuml_model_path = xuml_model_path
        self.flatland_layout_path = flatland_layout_path
        self.diagram_file_path = diagram_file_path
        self.rebuild = rebuild
        self.show_grid = show_grid
        self.no_color = no_color

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

        # Index all transitions by state
        cp = self.layout.connector_placement
        cp_dict = {}
        for c in cp:
            tstem = c.get('tstem')
            if tstem:
                k = tstem['node_ref']
            else:
                k = c['ustem']['node_ref']
            if cp_dict.get(k):
                cp_dict[k].append(c)
            else:
                cp_dict[k] = [c]

        # If there are any transitions, draw them
        if not nodes_only:
            self.logger.info("Drawing the transitions")
            for s in self.statemodel.states:
                try:
                    state_place = cp_dict[s.name]  # State placement (layout) info
                except KeyError:
                    self.logger.error(f'Transition from state [{s.name}] has no corresponding connector in layout file.')
                    sys.exit(1)
                if s.type == 'deletion':
                    it_place = [tp for tp in state_place if tp.get('ustem')][0]
                    self.draw_deletion_transition(cplace=it_place)
                if s.type == 'creation':
                    # It must have a unary creation transition
                    it_place = [tp for tp in state_place if tp.get('ustem')][0]
                    cname = make_event_cname(self.statemodel.events[s.creation_event])
                    self.draw_initial_transition(creation_event=cname, cplace=it_place)
                if s.transitions:
                    for t in s.transitions:
                        if len(t) == 2:  # Not CH or IG
                            evname = t[0]
                            cname = make_event_cname(self.statemodel.events[evname])
                            try:
                                t_place = [tp for tp in state_place if tp['cname'] == evname][0]
                            except IndexError:
                                self.logger.error(f'Model event [{cname}] does not name any connector in layout.')
                                sys.exit(1)
                            if t_place:
                                self.draw_transition(cname, t_place)

        self.logger.info("Rendering the Canvas")
        self.flatland_canvas.render()

    def draw_deletion_transition(self, cplace):
        """Draw a deletion transition to a final pseudo-state"""
        ustem = cplace['ustem']
        node_ref = ustem['node_ref']
        u_stem = New_Stem(stem_type='from deletion state', semantic='final pseudo state',
                          node=self.nodes[node_ref], face=ustem['face'],
                          anchor=ustem.get('anchor', None), stem_name=None)
        UnaryConnector(
            self.flatland_canvas.Diagram,
            connector_type_name='deletion transition',
            stem=u_stem,
            name=None
        )

    def draw_initial_transition(self, creation_event, cplace):
        """Draw an initial transition (with or without a creation event)"""
        ustem = cplace['ustem']
        node_ref = ustem['node_ref']
        u_stem = New_Stem(stem_type='to initial state', semantic='initial pseudo state',
                          node=self.nodes[node_ref], face=ustem['face'],
                          anchor=ustem.get('anchor', None), stem_name=None)
        evname_data = None if not creation_event else ConnectorName(
            text=creation_event, side=cplace['dir'], bend=cplace['bend'], notch=cplace['notch'])
        UnaryConnector(
            self.flatland_canvas.Diagram,
            connector_type_name='initial transition',
            stem=u_stem,
            name=evname_data
        )

    def draw_transition(self, evname, tlayout):
        """Draw a normal (non initial/non deletion transition)"""
        tstem = tlayout['tstem']
        pstem = tlayout['pstem']
        node_ref = tstem['node_ref']
        t_stem = New_Stem(stem_type='from state', semantic='source state',
                          node=self.nodes[node_ref], face=tstem['face'],
                          anchor=tstem.get('anchor', None), stem_name=None)
        node_ref = pstem['node_ref']
        p_stem = New_Stem(stem_type='to state', semantic='target state',
                          node=self.nodes[node_ref], face=pstem['face'],
                          anchor=pstem.get('anchor', None), stem_name=None)

        paths = None if not tlayout.get('paths', None) else \
            [New_Path(lane=p['lane'], rut=p['rut']) for p in tlayout['paths']]

        evname_data = ConnectorName(text=evname, side=tlayout['dir'], bend=tlayout['bend'], notch=tlayout['notch'])
        if not paths and OppositeFace[tstem['face']] == pstem['face']:
            StraightBinaryConnector(
                diagram=self.flatland_canvas.Diagram,
                connector_type='transition',
                t_stem=t_stem,
                p_stem=p_stem,
                name=evname_data
            )
        else:
            BendingBinaryConnector(
                diagram=self.flatland_canvas.Diagram,
                connector_type='transition',
                anchored_stem_p=p_stem,
                anchored_stem_t=t_stem,
                paths=paths,
                name=evname_data)

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
            no_color=self.no_color,
            color=lspec.color,
        )

    def draw_states(self) -> Dict[str, SingleCellNode]:
        """Draw all of the states on the state machine diagram"""

        nodes = {}
        np = self.layout.node_placement  # Layout data for all states

        for state in self.statemodel.states:

            # Get the state name from the model
            self.logger.info(f'Processing state: {state.name}')

            # Get the layout data for this state
            nlayout = np.get(state.name)
            if not nlayout:
                self.logger.warning(f"Skipping state [{state.name}] -- No placement specified in layout sheet")
                continue

            # Layout data for all placements
            # By default the state name is all on one line, but it may be wrapped across multiple
            nlayout['wrap'] = nlayout.get('wrap', 1)
            name_block = TextBlock(state.name, nlayout['wrap'])
            # Now assemble all the text content for each compartment
            text_content = [name_block.text, state.activity]

            for i, p in enumerate(nlayout['placements']):
                h = HorizAlign[p.get('halign', 'CENTER')]
                v = VertAlign[p.get('valign', 'CENTER')]
                expansion_percent = max(min(100, nlayout.get('node_expansion', 0)), 1)
                expansion_ratio = round(expansion_percent / 100, 2)
                # If this is an imported class, append the import reference to the attribute list
                row_span, col_span = p['node_loc']
                # If methods were supplied, include them in content
                # text content includes text for all compartments other than the title compartment
                # When drawing connectors, we want to attach to a specific node cplace
                # In most cases, this will just be the one and only indicated by the node name
                # But if a node is duplicated, i will not be 0 and we add a suffix to the node
                # name for the additional cplace
                node_name = state.name if i == 0 else f'{state.name}_{i + 1}'
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
