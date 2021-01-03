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

