"""
xUML_class_diagram.py – Generates an xuml diagram for an xuml model using the Flatland draw engine
"""

import sys
from pathlib import Path
from flatland.flatland_exceptions import FlatlandIOException, MultipleFloatsInSameBranch
from flatland.input.model_parser import ModelParser

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

        print("drawing a pretty diagram now. (Not really, but soon!)")
        print(f"from model: {self.xuml_model_path}")
        print(f"using layout: {self.flatland_layout_path}")
        print(f"to output file : {self.diagram_file_path}")
