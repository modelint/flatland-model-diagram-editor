"""
config.py - Configures flatland and rebuilds the database
"""
import yaml
import logging
import sys
from pathlib import Path
import inspect
from flatland.database.flatlanddb import FlatlandDB
from flatland.sheet_subsystem.titleblock_placement import TitleBlockPlacement
from typing import Dict
from collections import namedtuple

TableSpec = namedtuple("TableSpec", "name header folder")


class Config:
    """
    Here we overlay user configuration on top of built in system configuration.
    """
    logger = logging.getLogger(__name__)
    # Structure of each Flatland DB table holding configurable system/user data
    tables = [
        TableSpec(name="color", header=["Name", "R", "G", "B", "Canvas"], folder="drawing"),
    ]

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
        FlatlandDB(rebuild=rebuild_db)

        # Regen title blocks and insert into the flatland database
        # TODO: Make this part of the population update
        if rebuild_db:
            TitleBlockPlacement()


def update_populations():
    """
    Generate database population _instances.py files for each table containing any user configurable attributes
    These need to be generated before the database is rebuilt since it will use these files to load the db
    """
    Config.logger.info("Updating user configurable instance populations...")

    for table in Config.tables:
        # Load system configuration values first
        system_config_file = Config.system_config_home / f'{table.name}.yaml'
        try:
            with open(system_config_file, 'r') as scf:
                system_config_dict = yaml.load(scf, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            Config.logger.error(f"System config file: [{system_config_file}] not found")
            sys.exit(1)

        # Now overlay any user configuration
        user_config_file = Config.user_config_home / f'{table.name}.yaml'
        try:
            with open(user_config_file, 'r') as ucf:
                user_config_dict = yaml.load(ucf, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            Config.logger.info(f"No user config file found. [{user_config_file}]  Using system config only.")
            user_config_dict = None
        gen_pop_file(
            tuples_dict=system_config_dict | ({} if not user_config_dict else user_config_dict),
            table=table,
        )


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
        key_attr_name = table.header[0]
        for tuple_key, tuple_data in tuples_dict.items():
            line = f'    {{"{key_attr_name}": "{tuple_key}", '
            for attr_name in table.header[1:]:
                line += f'"{attr_name}": {tuple_data[attr_name]}, '
            line = line.rstrip(", ") + '},\n'
            pop.write(line)
        pop.write(bottom)


if __name__ == '__main__':
    Config()
