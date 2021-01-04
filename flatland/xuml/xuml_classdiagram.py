"""
xUML_class_diagram.py – Generates an xuml diagram for an xuml model using the Flatland draw engine
"""

import sys
from pathlib import Path
from flatland.flatland_exceptions import FlatlandIOException, MultipleFloatsInSameBranch
from flatland.input.model_parser import ModelParser
from flatland.input.layout_parser import LayoutParser
from flatland.database.flatlanddb import FlatlandDB
from flatland.node_subsystem.canvas import Canvas
from flatland.node_subsystem.single_cell_node import SingleCellNode
from flatland.datatypes.geometry_types import Alignment, VertAlign, HorizAlign
from flatland.datatypes.command_interface import New_Stem, New_Path, New_Trunk_Branch, New_Offshoot_Branch, New_Branch_Set
from flatland.connector_subsystem.straight_binary_connector import StraightBinaryConnector
from flatland.connector_subsystem.bending_binary_connector import BendingBinaryConnector
from flatland.datatypes.connection_types import ConnectorName, OppositeFace, StemName
from flatland.text.text_block import TextBlock
from typing import Optional, Dict

class XumlClassDiagram:

    def __init__(self, xuml_model_path: Path, flatland_layout_path: Path, diagram_file_path: Path):
        """Constructor"""
        self.xuml_model_path = xuml_model_path
        self.flatland_layout_path = flatland_layout_path
        self.diagram_file_path = diagram_file_path

        print("Parsing the model")
        # Parse the model
        try:
            self.model = ModelParser(model_file_path=self.xuml_model_path, debug=True)
        except FlatlandIOException as e:
            sys.exit(e)
        self.subsys = self.model.parse()

        # Parse the layout
        try:
            self.layout = LayoutParser(layout_file_path=self.flatland_layout_path, debug=True)
        except FlatlandIOException as e:
            sys.exit(e)
        self.layout = self.layout.parse()

        # Load the flatland database
        self.db = FlatlandDB()

        # Draw the blank canvas of the appropriate size, diagram type and presentation style
        self.flatland_canvas = self.create_canvas()

        # Draw all of the classes
        self.nodes = self.draw_classes()

        # If there are any relationships, draw them
        if self.subsys.rels:
            cp = self.layout.connector_placement
            for r in self.subsys.rels:  # r is the model data without any layout info
                rnum = r['rnum']
                rlayout = cp[rnum]  # How this r is to be laid out on the diagram
                if 'superclass' in r.keys():
                    pass
                    #self.draw_generalization(rnum=rnum, generalization=r, tree_layout=rlayout)
                else:
                    self.draw_association(rnum=rnum, association=r, binary_layout=rlayout)

        self.flatland_canvas.render()

        print("drawing a pretty diagram now. (Not really, but soon!)")
        print(f"from model: {self.xuml_model_path}")
        print(f"using layout: {self.flatland_layout_path}")
        print(f"to output file : {self.diagram_file_path}")

    def create_canvas(self) -> Canvas:
        """Create a blank canvas"""
        lspec = self.layout.layout_spec
        return Canvas(
            diagram_type=lspec.dtype,
            presentation=lspec.pres,
            notation=lspec.notation,
            standard_sheet_name=lspec.sheet,
            orientation=lspec.orientation,
            drawoutput=self.diagram_file_path,
            show_margin=True
        )

    def draw_classes(self) -> Dict[str, SingleCellNode]:
        """Draw all of the classes on the class diagram"""
        nodes = {}
        np = self.layout.node_placement
        for c in self.subsys.classes:
            cname = c['name']
            nlayout = np[cname]
            nlayout['wrap'] = nlayout.get('wrap', 1)
            name_block = TextBlock(cname, nlayout['wrap'])
            h = HorizAlign[nlayout.get('halign', 'CENTER')]
            v = VertAlign[nlayout.get('valign', 'CENTER')]
            nodes[cname] = SingleCellNode(
                node_type_name='class',
                content=[name_block.text, c['attributes']],
                grid=self.flatland_canvas.Diagram.Grid,
                row=nlayout['node_loc'][0], column=nlayout['node_loc'][1],
                local_alignment=Alignment(vertical=v, horizontal=h)
            )
        return nodes
        # TODO:  Include method section in content
        # TODO:  Add support for axis offset on stem names

    def draw_association(self, rnum, association, binary_layout):
        """Draw the binary association"""
        # Straight or bent connector?
        tstem = binary_layout['tstem']
        pstem = binary_layout['pstem']
        astem = binary_layout.get('tertiary_node', None)
        t_side = association['t_side']
        t_phrase = StemName(
            text=TextBlock(t_side['phrase'], wrap=tstem['wrap']),
            side=tstem['stem_dir'], axis_offset=None, end_offset=None
        )
        t_stem = New_Stem(stem_type='class mult', semantic=t_side['mult'] + ' mult',
                          node=self.nodes[t_side['cname']], face=tstem['face'],
                          anchor=tstem.get('anchor', None), stem_name=t_phrase)
        p_side = association['p_side']
        p_phrase = StemName(
            text=TextBlock(p_side['phrase'], wrap=pstem['wrap']),
            side=pstem['stem_dir'], axis_offset=None, end_offset=None
        )
        p_stem = New_Stem(stem_type='class mult', semantic=p_side['mult'] + ' mult',
                          node=self.nodes[p_side['cname']], face=pstem['face'],
                          anchor=pstem.get('anchor', None), stem_name=p_phrase)
        if astem:
            a_stem = New_Stem(stem_type='associative mult', semantic=association['assoc_mult'] + ' mult',
                              node=self.nodes[association['assoc_cname']], face=astem['face'], anchor=astem.get('anchor', None),
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
            print("Straight connector")
        else:
            BendingBinaryConnector(
                diagram=self.flatland_canvas.Diagram,
                connector_type='binary association',
                anchored_stem_p=p_stem,
                anchored_stem_t=t_stem,
                tertiary_stem=a_stem,
                paths=paths,
                name=rnum_data)
