"""
Flatland Diagram Editor

Usage:
------
    $ flatland [-m model] [-l layout] [-d diagram]
"""
import sys
import argparse
from pathlib import Path
from xuml.XumlClassDiagram import XumlClassDiagram
from flatland import version

# Configure the expected parameters and actions for the argparse module
def parse(cl_input):
    parser = argparse.ArgumentParser(description='Flatland model diagram generator')
    parser.add_argument('-m', '--model', action='store', default='model.xmm',
                        help='xuml model file name defining model connectivity without any layout information')
    parser.add_argument('-l', '--layout', action='store', default='normal.mss',
                        help='Flatland layout file defining all layout information with light references to model file.')
    parser.add_argument('-d', '--diagram', action='store', default='diagram.pdf',
                        help='Name of file to generate, .pdf extension automatically added')
    return parser.parse_args(cl_input)


def main():
    print(f'Flatland version: {version}')
    # Parse the command line args
    args = parse(sys.argv[1:])

    # model file: This can be provided via standard input or specified as an argument
    if args.model:
        model_path = Path(args.model)
        if not model_path.is_file():
            print(f"Model file: {args.model} specified on command line not found")
            sys.exit()
    else:
        model_path = sys.stdin

    # output file: If no output file is specified, the generated diagram is provided as standard output
    # For now, the only output format is PDF
    if args.diagram:
        diagram_path = Path(args.diagram)
    else:
        diagram_path = sys.stdout

    # Generate the xuml class diagram (we don't do anything with the returned variable yet)
    class_diagram = XumlClassDiagram(
        xuml_model_path=model_path,
        flatland_layout_path=args.layout,
        diagram_file_path=diagram_path,
    )

    # print("Initializing database...")
    # import flatland.tests.build_db_test

    print("Testing style database...")
    import flatland.tests.styledb_test
    print("No problemo")


if __name__ == "__main__":
    main()