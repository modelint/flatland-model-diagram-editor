""" layout_parser.py """

from flatland.flatland_exceptions import LayoutGrammarFileOpen, LayoutFileOpen, LayoutFileEmpty, LayoutParseError
from flatland.input.layout_visitor import LayoutVisitor
from arpeggio import visit_parse_tree, NoMatch
from arpeggio.cleanpeg import ParserPEG
from pathlib import Path
import os
from collections import namedtuple
from flatland.input.nocomment import nocomment

DiagramLayout = namedtuple('DiagramLayout', 'layout_spec node_placement connector_placement')
LayoutSpec = namedtuple('LayoutSpec', 'dtype pres notation sheet orientation frame frame_presentation, padding')
NodePlacement = namedtuple('NodePlacement', 'wrap row column halign valign')
ConnPlacement = namedtuple('ConnPlacement', 'name_side bend t_data, p_data')
StemSpec = namedtuple('StemSpec', 'name_side wrap face node anchor_at')


class LayoutParser:
    """
    Parses a flatland diagram layout specification for a corresponding model file.

        Attributes

        - grammar_file -- (class based) Name of the system file defining the layout grammar
        - layout_file -- Name of user specified diagram layout specification file
    """
    grammar_file_name = "model_markup/layout.peg"
    grammar_file = Path(__file__).parent.parent / grammar_file_name
    root_rule_name = "diagram_layout"
    layout_dir = Path(__file__).parent.parent / "examples" / "layouts"

    def __init__(self, layout_file_path, debug=True):
        """
        Constructor

        :param layout_file_path: Where to find the user supplied layout file
        :param debug: Debug flag
        """
        self.debug = debug
        self.layout_file_path = layout_file_path

        # Read the grammar file
        try:
            self.layout_grammar = nocomment(open(LayoutParser.grammar_file, 'r').read())
        except OSError as e:
            raise LayoutGrammarFileOpen(LayoutParser.grammar_file)

        # Read the layout file
        try:
            self.layout_text = nocomment(open(self.layout_file_path, 'r').read())
        except OSError as e:
            raise LayoutFileOpen(self.layout_file_path)

        if not self.layout_text:
            raise LayoutFileEmpty(self.layout_file_path)

    def parse(self) -> DiagramLayout:
        """
        Parse the layout file and return the content
        :return: THe abstract syntax tree content of interest
        """
        # Create an arpeggio parser for our model grammar that does not eliminate whitespace
        # We interpret newlines and indents in our grammar, so whitespace must be preserved
        parser = ParserPEG(self.layout_grammar, LayoutParser.root_rule_name, skipws=False, debug=self.debug)
        # Now create an abstract syntax tree from our layout text
        try:
            parse_tree = parser.parse(self.layout_text)
        except NoMatch as e:
            raise LayoutParseError(self.layout_file_path.name, e) from None
        # Transform that into a result that is better organized with grammar artifacts filtered out
        result = visit_parse_tree(parse_tree, LayoutVisitor(debug=self.debug))
        if self.debug:
            # Transform dot files into pdfs
            peg_tree_dot = Path("peggrammar_parse_tree.dot")
            peg_model_dot = Path("peggrammar_parser_model.dot")
            parse_tree_dot = Path("diagram_layout_parse_tree.dot")
            parser_model_dot = Path("diagram_layout_peg_parser_model.dot")

            parse_tree_file = str(LayoutParser.layout_dir / self.layout_file_path.stem) + "_parse_tree.pdf"
            model_file = str(LayoutParser.layout_dir / self.layout_file_path.stem) + "_model.pdf"
            os.system(f'dot -Tpdf {parse_tree_dot} -o {parse_tree_file}')
            os.system(f'dot -Tpdf {parser_model_dot} -o {model_file}')
            # Cleanup unneeded dot files, we just use the PDFs for now
            parse_tree_dot.unlink(missing_ok=True)
            parser_model_dot.unlink(missing_ok=True)
            peg_tree_dot.unlink(missing_ok=True)
            peg_model_dot.unlink(missing_ok=True)
        # Refine parsed result into something more useful for the client
        ld = result.results['layout_spec'][0]  # layout data
        # Some items are optional
        frame = ld.get('frame')
        frame_presentation = ld.get('frame_presentation')
        padding = ld.get('padding')
        lspec = LayoutSpec(dtype=ld['diagram'][0], notation=ld['notation'][0], pres=ld['presentation'][0],
                           orientation=ld['orientation'][0], sheet=ld['sheet'][0],
                           frame=None if not frame else frame[0],
                           # frame_presentation not relevant if no frame
                           frame_presentation=None if not frame else frame_presentation[0],
                           padding=None if not padding else padding[0])

        node_pdict = {}
        for n in result.results['node_block'][0]:
            dup_num = n.get('duplicate')
            key = n['node_name'] if not dup_num else f"{n['node_name']}_{dup_num}"
            node_pdict[key] = n


        if 'connector_block' in result.results:
            conn_pdict = { c['cname']: c for c in result.results['connector_block'][0] }
        else:
            conn_pdict = None
        return DiagramLayout(layout_spec=lspec, node_placement=node_pdict, connector_placement=conn_pdict)



if __name__ == "__main__":
    # For diagnostics
    layout_path = Path(__file__).parent.parent / 'Test/t052_rbranch_vert_corner.mss'
    x = LayoutParser(layout_file_path=layout_path, debug=True)
    x.parse()