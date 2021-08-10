"""
config.py - Configures flatland and rebuilds the database
"""
import yaml
import textwrap
import logging
import sys
from pathlib import Path
import inspect
from flatland.database.flatlanddb import FlatlandDB
from flatland.sheet_subsystem.titleblock_placement import TitleBlockPlacement
from typing import Dict, List
from collections import namedtuple

TableSpec = namedtuple("TableSpec", "header folder")

def update_populations():
    """
    Generate database population _instances.py files for each table containing any user configurable attributes
    These need to be generated before the database is rebuilt since it will use these files to load the db
    """
    Config.logger.info("Updating user configurable instance populations...")

    for config_file, popfunc in Config.populator.items():
        # Load system configuration values first
        system_config_file = Config.system_config_home / f'{config_file}.yaml'
        try:
            with open(system_config_file, 'r') as scf:
                system_config_dict = yaml.load(scf, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            Config.logger.error(f"System config file: [{system_config_file}] not found")
            sys.exit(1)

        # Now overlay any user configuration
        user_config_file = Config.user_config_home / f'{config_file}.yaml'
        try:
            with open(user_config_file, 'r') as ucf:
                user_config_dict = yaml.load(ucf, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            Config.logger.info(f"No user config file found. [{user_config_file}]  Using system config only.")
            user_config_dict = None

        overlayed_config_dict = system_config_dict | ({} if not user_config_dict else user_config_dict),

        pop_lines = popfunc(
            config_data=overlayed_config_dict,
        )
        write_pop_files(pop_lines)

def gen_pop_file(tuples_dict: Dict[str, str], table: TableSpec):
    """
    Generate a population file to be loaded by the database

    :param tuples_dict: A dictionary of named tuples where each tuple can be inserted into a table
    :param table: The configuration table spec so we know how to format the population file
    """
    pop_fname = f'{table.name}_instances.py'
    # The top and bottom text in the generated population file
    top = inspect.cleandoc(f'''"""
    {pop_fname} (generated)
    """
    population = [
    ''') + '\n'
    bottom = ']'

    pop_path = Config.pop_home / table.folder / pop_fname

    with open(pop_path, 'w') as pop:
        pop.write(top)
        key_attr_name, key_attr_type = table.header[0]
        for tuple_key, tuple_data in tuples_dict.items():
            tuple_key_value = f'"{tuple_key}"' if key_attr_type is str else tuple_key
            line = f'    {{"{key_attr_name}": {tuple_key_value}, '
            for attr_name, attr_type in table.header[1:]:
                attr_value = f'"{tuple_data[attr_name]}"' if attr_type is str else tuple_data[attr_name]
                line += f'"{attr_name}": {attr_value}, '
            line = line.rstrip(", ") + '},\n'
            pop.write(line)
        pop.write(bottom)

def write_pop_files(pop_lines: Dict[str, List[str]]):
    """

    :param pop_lines:
    :return:
    """
    for name, lines in pop_lines.items():
        pop_fname = f'{name}_instances.py'
        # The top and bottom text in the generated population file
        top = inspect.cleandoc(f'''"""
        {pop_fname} (generated)
        """
        population = [
        ''') + '\n'
        bottom = '\n]\n'

        pop_path = Config.pop_home / Config.tables[name].folder / pop_fname
        with open(pop_path, 'w') as pop:
            pop.write(top)
            text = '\n'.join(lines)
            itext = textwrap.indent(text, '    ')

            pop.write(itext)
            pop.write(bottom)
        pass


def gen_frame_pop(config_data: tuple) -> Dict[str, List[str]]:
    """
    Generate python output data for the frame, open_field and titlebock_placement instance population files
    from a single parsed frame.yaml file input file

    :param config_data: Parse output from system/user combined frame.yaml configuration file
    :return: Dictionary with { table_name : lines_to_write } for each output yaml file
    """
    frame_lines = []
    field_lines = []
    title_block_placement_lines = []

    for frame_dict in config_data:
        for frame_name, sheets in frame_dict.items():
            for sheet_dict in sheets:
                o = sheet_dict["Orientation"]
                s = sheet_dict["Sheet"]
                frame_line = f'{{"Name": "{frame_name}", "Sheet": "{s}", "Orientation": "{o}"}},'
                frame_lines.append(frame_line)
                for fkey, field_dict in sheet_dict["Fields"].items():
                    field_lines.append(
                        f'{{"Metadata": "{fkey}", "Frame": "{frame_name}", "Sheet": "{s}", "Orientation": "{o}",')
                    field_lines.append(
                        f' "x position": {field_dict["X"]}, "y position": {field_dict["Y"]}, '
                        f'"max width": {field_dict["Max width"]}, "max height": {field_dict["Max height"]}}},')
                tb_dict = sheet_dict.get("Title block")
                if tb_dict:  # Not all frames use a title block
                    title_block_placement_lines.append(
                        f'{{"Frame": "{frame_name}", "Sheet": "{s}", "Orientation": "{o}",')
                    title_block_placement_lines.append(
                        f' "Title block pattern": "{tb_dict["Name"]}", "Sheet size group": "{None}", "X": {tb_dict["X"]}, "Y": {tb_dict["Y"]}}},')
    return {"frame": frame_lines, "open_field": field_lines, "titleblock_placement": title_block_placement_lines}



class Config:
    """
    Here we overlay user configuration on top of built in system configuration.
    """
    logger = logging.getLogger(__name__)

    # Yaml configuration files to be loaded
    populator = { "frame": gen_frame_pop }  # , "sheet": gen_pop_file, "color": gen_pop_file, }

    # Structure of each Flatland DB table to be populated from config data
    tables = {
        "frame": TableSpec(header=[("Name", str), ("Sheet", str), ("Orientation", str)], folder="sheet"),
        "open_field": TableSpec(
            header=[("Metadata", str), ("Frame", str), ("Sheet", str), ("Orientation", str),
                    ("x position", int), ("y position", int), ("max width", int), ("max height", int),
                    ], folder='sheet'),
        "titleblock_placement": TableSpec(
                  header=[("Frame", str), ("Sheet", str), ("Orientation", str), ("Title block pattern", str),
                          ("Sheet size group", str), ("X", int), ("Y", int)],
                  folder='sheet'),
        "color": TableSpec(header=[("Name", str), ("R", int), ("G", int), ("B", int), ("Canvas", bool) ],
                  folder="drawing"),
        "sheet": TableSpec(header=[("Name", str), ("Group", str), ("Height", float), ("Width", float),
                                        ("Size group", str)], folder="sheet"),
    }

    # Where we look for system configuration data
    system_config_home = Path(__file__).parent

    # Where we look for the user supplied configuration data, if any
    user_config_home = Path.home() / '.flatland' / 'config'

    # Population home
    pop_home = Path(__file__).parent.parent / "database" / "population"

    def __init__(self, rebuild_db: bool = True):
        """
        Perform all configuration tasks required before the app starts

        :param rebuild_db: True if the database needs to be rebuilt
        """
        if rebuild_db:
            # Before rebuilding, generate any new instance population files
            update_populations()

        # Initialize and possible reload the flatland database
        # FlatlandDB(rebuild=rebuild_db)

        # Regen title blocks and insert into the flatland database
        # TODO: Make this part of the population update
        # if rebuild_db:
        #     TitleBlockPlacement()






if __name__ == '__main__':
    Config()
