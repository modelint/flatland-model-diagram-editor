"""
Flatland Diagram Editor

"""
import logging
import logging.config
import sys
import atexit
import argparse
from pathlib import Path
from flatland.xuml.xuml_classdiagram import XumlClassDiagram
from flatland.xuml.xuml_statemachine_diagram import XumlStateMachineDiagram
from flatland.configuration.config import Config
from flatland import version

_logpath = Path("flatland.log")


def clean_up():
    """Normal and exception exit activities"""
    _logpath.unlink(missing_ok=True)

def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module

# Configure the expected parameters and actions for the argparse module
def parse(cl_input):
    parser = argparse.ArgumentParser(description='Flatland model diagram generator')
    parser.add_argument('-m', '--model', action='store',
                        help='xuml model file name defining model connectivity without any layout information')
    parser.add_argument('-l', '--layout', action='store',
                        help='Flatland layout file defining all layout information with light\
                         references to model file.')
    parser.add_argument('-d', '--diagram', action='store', default='diagram.pdf',
                        help='Name of file to generate, .pdf extension automatically added')
    parser.add_argument('-D', '--docs', action='store_true',
                        help='Copy the project documentation directory into the local directory')
    parser.add_argument('-CF', '--config', action='store_true',
                        help="Create a new config directory in user's flatland home")
    parser.add_argument('-E', '--examples', action='store_true',
                        help='Create a directory of examples in the current directory')
    parser.add_argument('-L', '--log', action='store_true',
                        help='Generate a diagnostic flatland.log file')
    parser.add_argument('-N', '--nodes_only', action='store_true',
                        help='Do not draw any connectors. Helpful to diagnose connector failures due\
                         to bad node cplace.')
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
    # Start logging
    logger = get_logger()
    logger.info(f'Flatland version: {version}')

    # Keep track of whether or not Config has been run by some command line option so we don't re-run it
    already_configured = False

    # Parse the command line args
    args = parse(sys.argv[1:])

    if not args.log:
        # If no log file is requested, remove the log file before termination
        atexit.register(clean_up)

    if args.version:
        # Just print the version and quit
        print(f'Flatland version: {version}')
        sys.exit(0)

    if args.colors:
        # Just print the database colors and quit
        Config(rebuild_db=args.rebuild)  # Do any configuration tasks necessary before starting up the app
        already_configured = True  # Don't run it again
        from flatland.drawing_domain.styledb import StyleDB
        StyleDB(print_colors=True)

    if args.config:
        # Copy user startup config files to their .flatland/config dir, creating it if it doesn't yet exist
        import shutil
        user_home = Path.home() / '.flatland'
        user_config_home = user_home / 'config'
        user_config_home.mkdir(parents=True, exist_ok=True)
        user_startup = Path(__file__).parent / 'configuration' / 'user_startup'
        for f in user_startup.iterdir():
            if not (user_config_home / f.name).exists():
                shutil.copy(f, user_config_home)

    if args.examples:
        # Copy the entire example directory into the users local dir if it does not already exist
        import shutil
        ex_path = Path(__file__).parent / 'examples'
        local_ex_path = Path.cwd() / 'examples'
        if local_ex_path.exists():
            logger.warning("Examples already exist in the current directory. Delete or move it if you want the latest.")
        else:
            logger.info("Copying example directory users local directory")
            shutil.copytree(ex_path, local_ex_path)  # Copy the example directory
            test_gen_path = Path(__file__).parent / 'tests' / 'gen_example_diagrams.py'
            shutil.copy(test_gen_path, local_ex_path)  # Copy the gen_example file into the copied example dir

    if args.docs:
        # Copy the entire docs directory into the users local dir if it does not already exist
        import shutil
        docs_path = Path(__file__).parent / 'documentation'
        local_docs_path = Path.cwd() / 'documentation'
        if local_docs_path.exists():
            logger.warning("Documentation already exists in the current directory.\
             Delete or move it if you want the latest.")
        else:
            logger.info("Copying doc directory to users local directory")
            shutil.copytree(docs_path, local_docs_path)

    if args.model and not args.layout:
        logger.error("A layout file must be specified for your model.")
        sys.exit(1)

    if args.layout and not args.model:
        logger.error("A model file must be specified to layout.")
        sys.exit(1)

    # At this point we either have both model and layout or neither
    # If neither, the only thing we might do at this point is rebuild the database if requested

    # Do any configuration tasks necessary before starting up the app
    # The database will be rebuilt if requested
    if not already_configured:
        Config(rebuild_db=args.rebuild)

    if args.model and args.layout:  # Just making sure we have them both
        model_path = Path(args.model)
        layout_path = Path(args.layout)
        diagram_path = Path(args.diagram)

        # Generate the xuml class diagram (we don't do anything with the returned variable yet)
        mtype = model_path.suffix
        if mtype == '.xmm' or mtype == '.xcm':
            class_diagram = XumlClassDiagram(
                xuml_model_path=model_path,
                flatland_layout_path=layout_path,
                diagram_file_path=diagram_path,
                show_grid=args.grid,
                nodes_only=args.nodes_only,
                no_color=args.no_color,
            )
        elif mtype == '.xsm':
            statemodel_diagram = XumlStateMachineDiagram(
                xuml_model_path=model_path,
                flatland_layout_path=layout_path,
                diagram_file_path=diagram_path,
                show_grid=args.grid,
                nodes_only=args.nodes_only,
                no_color=args.no_color,
            )

    logger.info("No problemo")  # We didn't die on an exception, basically


if __name__ == "__main__":
    main()
