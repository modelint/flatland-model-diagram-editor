"""
Flatland Diagram Editor

"""
import logging
import logging.config
import sys
import argparse
from pathlib import Path
from flatland.xuml.xuml_classdiagram import XumlClassDiagram
from flatland.xuml.xuml_statemachine_diagram import XumlStateMachineDiagram
from flatland import version

def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module

# Configure the expected parameters and actions for the argparse module
def parse(cl_input):
    parser = argparse.ArgumentParser(description='Flatland model diagram generator')
    parser.add_argument('-m', '--model', action='store', default='model.xmm',
                        help='xuml model file name defining model connectivity without any layout information')
    parser.add_argument('-l', '--layout', action='store', default='normal.mls',
                        help='Flatland layout file defining all layout information with light references to model file.')
    parser.add_argument('-d', '--diagram', action='store', default='diagram.pdf',
                        help='Name of file to generate, .pdf extension automatically added')
    parser.add_argument('-D', '--docs', action='store_true',
                        help='Copy the project documentation directory into the local directory')
    parser.add_argument('-E', '--examples', action='store_true',
                        help='Create a directory of examples in the current directory')
    parser.add_argument('-L', '--log', action='store_true',
                        help='Generate a diagnostic flatland.log file')
    parser.add_argument('-N', '--nodes_only', action='store_true',
                        help='Do not draw any connectors. Helpful to diagnose connector failures due to bad node cplace.')
    parser.add_argument('-NC', '--no_color', action='store_true',
                        help='Use white instead of the specified sheet color. Useful when creating printer output.'),
    parser.add_argument('-V', '--version', action='store_true',
                        help='Print the current version of flatland')
    parser.add_argument('-G', '--grid', action='store_true',
                        help='Print the grid so you can diagnose output with row and column boundaries visible')
    parser.add_argument('-R', '--rebuild', action='store_true',
                        help='Rebuild the flatland database. Necessary only if corrupted.')
    parser.add_argument('-COLORS', '--colors', action='store_true',
                        help='Show the list of background color names')
    return parser.parse_args(cl_input)


def main():
    logger = get_logger()
    args = parse(sys.argv[1:])

    if args.version:
        print(f'Flatland version: {version}')
        sys.exit(0)

    if args.colors:
        from flatland.drawing_domain.styledb import StyleDB
        StyleDB(print_colors=True, rebuild=args.rebuild)
        sys.exit(0)

    if args.examples or args.docs:
        # Make a local copy of the examples and/or documentation directories for the user
        import shutil
        ex_path = Path(__file__).parent / 'examples'
        docs_path = Path(__file__).parent / 'documentation'
        local_ex_path = Path.cwd() / 'examples'
        local_docs_path = Path.cwd() / 'documentation'
        if args.examples:
            if local_ex_path.exists():
                logger.info("examples already exist in the current directory.")
                if not args.docs:
                    sys.exit(1)
            else:
                shutil.copytree(ex_path, local_ex_path)  # Copy the example directory
                test_gen_path = Path(__file__).parent / 'tests' / 'gen_example_diagrams.py'
                shutil.copy(test_gen_path, local_ex_path)  # Copy the gen_example file into the copied example dir
        if args.docs:
            if local_docs_path.exists():
                logger.error("documentation already exists in the current directory.")
                sys.exit(1)
            import shutil
            shutil.copytree(docs_path, local_docs_path)
        sys.exit(0)

    logger.info(f'Flatland version: {version}')
    # Parse the command line args

    # model file: This can be provided via standard input or specified as an argument
    if args.model:
        model_path = Path(args.model)
        if not model_path.is_file():
            logger.error(f"Model file: {args.model} specified on command line not found")
            sys.exit(1)
    else:
        # TODO: Standard input is not yet supported, so this is a placeholder
        # TODO: Since a default model file is always supplied via argparse above, this clause will never execute
        model_path = sys.stdin

    # layout file: This must be supplied via an argument or the default layout file is presumed
    layout_path = Path(args.layout)
    if not layout_path.is_file():
        logger.error(f"Layout file: {args.layout} specified on command line not found")
        sys.exit(1)

    # output file: If no output file is specified, the generated diagram is provided as standard output
    # For now, the only output format is PDF
    if args.diagram:
        diagram_path = Path(args.diagram)
    else:
        # TODO: Standard output is not yet supported, so this is a placeholder
        # TODO: Since a default diagram file is always supplied via argparse above, this clause will never execute
        diagram_path = sys.stdout

    # Generate the xuml class diagram (we don't do anything with the returned variable yet)
    mtype = model_path.suffix
    if mtype == '.xmm' or mtype == '.xcm':
        class_diagram = XumlClassDiagram(
            xuml_model_path=model_path,
            flatland_layout_path=layout_path,
            diagram_file_path=diagram_path,
            rebuild=args.rebuild,
            show_grid=args.grid,
            nodes_only=args.nodes_only,
            no_color=args.no_color,
        )
    elif mtype == '.xsm':
        statemodel_diagram = XumlStateMachineDiagram(
            xuml_model_path=model_path,
            flatland_layout_path=layout_path,
            diagram_file_path=diagram_path,
            rebuild=args.rebuild,
            show_grid=args.grid,
            nodes_only=args.nodes_only,
            no_color=args.no_color,
        )

    logger.info("No problemo")  # We didn't die on an exception, basically

    if not args.log:
        # If we didn't crash and no log is explicitly requested, delete it
        logpath = Path("flatland.log")
        logpath.unlink(missing_ok=True)

if __name__ == "__main__":
    main()