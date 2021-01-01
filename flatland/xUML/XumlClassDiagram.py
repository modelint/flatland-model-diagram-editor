"""
xUML_class_diagram.py – Generates an xUML diagram for an xUML model using the Flatland draw engine
"""

from pathlib import Path

class XumlClassDiagram:

    def __init__(self, xuml_model_path: Path, flatland_layout_path: Path, diagram_file_path: Path):
        """Constructor"""
        self.xuml_model_path = xuml_model_path
        self.flatland_layout_path = flatland_layout_path
        self.diagram_file_path = diagram_file_path

        print("Drawing a pretty diagram now. (Not really, but soon!)")
        print(f"from model: {self.xuml_model_path}")
        print(f"using layout: {self.flatland_layout_path}")
        print(f"to output file : {self.diagram_file_path}")
