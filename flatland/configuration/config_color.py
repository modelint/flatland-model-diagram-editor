"""
config_color.py – Load color yaml file and generate a population dictionary
"""
import yaml
from pathlib import Path

config_path = Path(__file__).parent
color_path = config_path / 'system_colors.yaml'
# config_path = Path.home() / '.flatland' / 'config'
# color_path = config_path / 'colors.yaml'

top = f'''"""
color_instances.py
"""
population = [
'''
bottom = ']'

def config_color():
    with open(color_path) as f:
        color_dict = yaml.load(f, Loader=yaml.FullLoader)
        make_color_pop(color_dict)

def make_color_pop(color_dict):
    with open(config_path / 'color_pop.py', 'w') as p:
        p.write(top)
        for k,v in color_dict.items():
            line = f'    {{"Name": "{k}", "R": {v["R"]}, "G": {v["G"]}, "B": {v["B"]}, "Canvas": {v["Canvas"]}}},\n'
            p.write(line)
        p.write(bottom)


config_color()