"""
config_color.py – Load color yaml file and generate a population dictionary
"""
import sys
import yaml
from pathlib import Path

# Home of system and user config files
system_config_home = Path(__file__).parent
user_config_home = Path.home() / '.flatland' / 'config'

# System and user color config paths
color_config = 'colors.yaml'
system_colors = system_config_home / color_config
user_colors = user_config_home / color_config

# Color population file
color_pop = system_config_home / 'color_instances.py'

top = f'''"""
color_instances.py
"""
population = [
'''
bottom = ']'

def config_color():
    # Load system colors first
    try:
        with open(system_colors, 'r') as sc:
            system_color_dict = yaml.load(sc, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print("No system colors file!")
        sys.exit(1)

    # Overlay and add user colors if any user colors are specified
    try:
        with open(user_colors, 'r') as uc:
            user_color_dict = yaml.load(uc, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print(f"No user color config file found. [{user_colors}]  Using system colors only.")
        user_color_dict = None
    make_color_pop(system_color_dict | {} if not user_color_dict else user_color_dict)

def make_color_pop(color_dict):
    with open(color_pop, 'w') as pop:
        pop.write(top)
        for k, v in color_dict.items():
            line = f'    {{"Name": "{k}", "R": {v["R"]}, "G": {v["G"]}, "B": {v["B"]}, "Canvas": {v["Canvas"]}}},\n'
            pop.write(line)
        pop.write(bottom)


config_color()
