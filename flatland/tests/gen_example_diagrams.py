"""
gen_example_diagrams.py – Here we generate all or some of the examples
"""
from flatland.xuml.xuml_classdiagram import XumlClassDiagram
from flatland import version
from pathlib import Path
import logging
import logging.config
from datetime import datetime

def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent.parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module

# Here we map the test code to a tuple defining the model and layout file
# combination to test
tests = {
    # Binary connectors (associations)
    't001': ('aircraft2', 't001_straight_binary_horiz'),
    't002': ('aircraftpilot_compsym', 't001_straight_binary_horiz.py'),
    't003': ('aircraft2', 't003_straight_binary_vert'),
    't004': ('tall_class', 't004_single_cell_node_tall'),
    't005': ('aircraft2', 't005_bending_binary_one'),
    't006': ('aircraft2', 't006_reverse_straight_binary_horiz'),
    't007': ('aircraft2', 't007_straight_binary_horiz_offset'),
    't008': ('widenode2', 't008_wide_node_stack'),
    't009': ('thin_node', 't009_expand'),
    't010': ('fat_class', 't010_spanning_node_ll_corner'),
    't011': ('tall_class', 't011_spanning_node_middle_tall'),
    't012': ('fat_class', 't012_spanning_node_middle_wide'),
    't013': ('tall_class', 't013_spanning_node_middle_tall_wide'),
    't014': ('tall_class', 't014_spanning_node_middle_align'),
    't015': ('many_associative', 't015_compound_adjacent_deckstack'),
    't016': ('aircraft2', 't016_imports'),
    't020': ('aircraft2', 't020_bending_binary_horiz'),
    't021': ('aircraft2', 't021_bending_binary_vert'),
    't022': ('aircraft2', 't022_bending_binary_horizontal_d1'),
    't023': ('aircraft2', 't023_bending_binary_twice'),
    't025': ('waypoint', 't025_reflexive_upper_right'),
    't026': ('aircraft2', 't026_single_bend_binary'),
    't030': ('aircraft3', 't030_straight_binary_tertiary'),
    't031': ('aircraft3', 't031_straight_binary_tertiary_horizontal'),
    't032': ('aircraft3', 't032_1bend_tertiary_left'),
    't033': ('aircraft3', 't033_2bend_tertiary_below'),
    't034': ('aircraft3', 't034_2bend_tertiary_above'),
    't035': ('aircraft3', 't035_2bend_tertiary_right'),
    't036': ('aircraft3', 't036_2bend_tertiary_left'),
    # Tree connectors (generalization)
    't040': ('aircraft_tree1', 't040_ibranch_horiz'),
    't041': ('aircraft_tree1', 't041_ibranch_vert'),
    't042': ('aircraft_tree1', 't042_ibranch_horiz_span'),
    't043': ('aircraft_tree_wrap', 't043_ibranch_wrap'),
    't050': ('aircraft_tree1', 't050_rbranch_horiz'),
    't051': ('aircraft_tree1', 't051_rbranch_vert'),
    't052': ('aircraft_tree2', 't052_rbranch_vert_corner'),
    't053': ('aircraft_tree1', 't053_p1_rbranch_vertical'),
    't054': ('aircraft_tree3', 't054_p2_gbranch_no_float'),
    't055': ('aircraft_tree4', 't055_p2_three_branch_one_graft'),
    't056': ('aircraft_tree4', 't056_p3_single_branch_graft_float'),
    't057': ('aircraft_tree4', 't057_p5_single_branch_grafted_from_trunk'),
    't058': ('aircraft_tree4', 't058_p5_single_branch_grafted_from_trunk_left'),
    't100': ('flatland_node_subsystem', 't100_flatland_node_subsystem'),
}

logger = get_logger()
logger.info(f'Flatland testing log: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
logger.info(f'Flatland version: {version}')

exdir = Path(__file__).parent.parent / "examples"

selected_tests = ['t016']  # Selected tests to run, if any
#selected_tests = ['t010', 't011', 't012', 't013']  # Selected tests to run, if any
# If no tests are selected, all of them will be run
run_tests = selected_tests if selected_tests else list(tests.keys())

for selected_test in run_tests:
    # We using the selected_test key, we compose our model and layout file names
    model_file_path = (exdir / "xuml_models" / tests[selected_test][0]).with_suffix(".xmm")
    layout_file_path = (exdir / "layouts" / tests[selected_test][1]).with_suffix(".mls")

    # The diagram output will always go into this file for visual inspection
    diagram_file_path = (exdir / "diagrams" / selected_test).with_suffix(".pdf")

    # Generate the xUML class diagram
    # This is the same command that would be triggered from the command line wrapper
    cd = XumlClassDiagram(
        xuml_model_path=model_file_path,
        flatland_layout_path=layout_file_path,
        diagram_file_path=diagram_file_path,
        rebuild=False,
        show_grid=True,
        nodes_only=False,
        no_color=False,
    )