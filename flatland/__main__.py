"""
Flatland Diagram Editor

Usage:
------
    $ flatland [-h] [-m model] [-l layout] [-d diagram]
"""
import logging
import logging.config
import sys
import argparse
from pathlib import Path
from flatland.xuml.xuml_classdiagram import XumlClassDiagram
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
    parser.add_argument('-l', '--layout', action='store', default='normal.mss',
                        help='Flatland layout file defining all layout information with light references to model file.')
    parser.add_argument('-d', '--diagram', action='store', default='diagram.pdf',
                        help='Name of file to generate, .pdf extension automatically added')
    parser.add_argument('-R', '--rebuild', action='store_true',
                        help='Rebuild the flatland database. Necessary only if corrupted.')
    return parser.parse_args(cl_input)


def main():
    logger = get_logger()
    logger.info(f'Flatland version: {version}')
    # Parse the command line args
    args = parse(sys.argv[1:])

    # model file: This can be provided via standard input or specified as an argument
    if args.model:
        model_path = Path(args.model)
        if not model_path.is_file():
            logger.error(f"Model file: {args.model} specified on command line not found")
            sys.exit()
    else:
        # TODO: Standard input is not yet supported, so this is a placeholder
        # TODO: Since a default model file is always supplied via argparse above, this clause will never execute
        model_path = sys.stdin

    # layout file: This must be supplied via an argument or the default layout file is presumed
    layout_path = Path(args.layout)
    if not layout_path.is_file():
        logger.error(f"Layout file: {args.layout} specified on command line not found")
        sys.exit()

    # output file: If no output file is specified, the generated diagram is provided as standard output
    # For now, the only output format is PDF
    if args.diagram:
        diagram_path = Path(args.diagram)
    else:
        # TODO: Standard output is not yet supported, so this is a placeholder
        # TODO: Since a default diagram file is always supplied via argparse above, this clause will never execute
        diagram_path = sys.stdout

    # Make a Diagnostics directory if it doesn't exist
    Path('Diagnostics').mkdir(parents=True, exist_ok=True)

    # Generate the xuml class diagram (we don't do anything with the returned variable yet)
    class_diagram = XumlClassDiagram(
        xuml_model_path=model_path,
        flatland_layout_path=layout_path,
        diagram_file_path=diagram_path,
        rebuild=args.rebuild
    )

    logger.info("No problemo")  # We didn't die on an exception, basically


if __name__ == "__main__":
    main()