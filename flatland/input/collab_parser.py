""" collab_parser.py - parse xUML class collaboration view specification"""

from flatland.flatland_exceptions import ModelGrammarFileOpen, ModelInputFileOpen, ModelInputFileEmpty
from flatland.flatland_exceptions import ModelParseError
from flatland.input.collab_visitor import CollaborationVisitor
from arpeggio import visit_parse_tree, NoMatch
from arpeggio.cleanpeg import ParserPEG
from collections import namedtuple
from flatland.input.nocomment import nocomment
import os
from pathlib import Path

Collaboration = namedtuple('Collaboration', 'metadata domain actors interactions')

class CollabParser:
    """
    Parses an Executable UML collaboration view input file using the arpeggio parser generator

        Attributes

        - grammar_file -- (class based) Name of the system file defining the Executable UML grammar
        - root_rule_name -- (class based) Name of the top level grammar element found in grammar file
        - debug -- debug flag (used to set arpeggio parser mode)
        - view_grammar -- The view grammar text read from the system grammar file
        - view_text -- The input view text read from the user supplied text file
    """
    grammar_file_name = "model_markup/collaboration.peg"
    grammar_file = Path(__file__).parent.parent / grammar_file_name
    root_rule_name = 'collaboration'  # We don't draw a diagram larger than a single domain
    xuml_view_dir = Path(__file__).parent.parent / "examples" / "road"

    def __init__(self, view_file_path, debug=True):
        """
        Constructor

        :param view_file_path:  Where to find the user supplied view input file
        :param debug:  Debug flag
        """
        self.debug = debug
        self.view_file_path = view_file_path

        # Read the grammar file
        try:
            self.view_grammar = nocomment(open(CollabParser.grammar_file, 'r').read())
        except OSError as e:
            raise ModelGrammarFileOpen(CollabParser.grammar_file)

        # Read the view file
        try:
            self.view_text = nocomment(open(self.view_file_path, 'r').read())
        except OSError as e:
            raise ModelInputFileOpen(self.view_file_path)

        if not self.view_text:
            raise ModelInputFileEmpty(self.view_file_path)

    def parse(self) -> Collaboration:
        """
        Parse the model file and return the content
        :return:  The abstract syntax tree content of interest
        """
        # Create an arpeggio parser for our model grammar that does not eliminate whitespace
        # We interpret newlines and indents in our grammar, so whitespace must be preserved
        parser = ParserPEG(self.view_grammar, CollabParser.root_rule_name, skipws=False, debug=self.debug)
        # Now create an abstract syntax tree from our model text
        try:
            parse_tree = parser.parse(self.view_text)
        except NoMatch as e:
            raise ModelParseError(self.view_file_path.name, e) from None
        # Transform that into a result that is better organized with grammar artifacts filtered out
        result = visit_parse_tree(parse_tree, CollaborationVisitor(debug=self.debug))
        # Make it even nicer using easy to reference named tuples
        if self.debug:
            # Transform dot files into pdfs
            peg_tree_dot = Path("peggrammar_parse_tree.dot")
            peg_model_dot = Path("peggrammar_parser_model.dot")
            parse_tree_dot = Path("statemodel_parse_tree.dot")
            parser_model_dot = Path("statemodel_peg_parser_model.dot")

            parse_tree_file = str(CollabParser.xuml_view_dir / self.view_file_path.stem) + "_parse_tree.pdf"
            view_file = str(CollabParser.xuml_view_dir / self.view_file_path.stem) + "_view.pdf"
            os.system(f'dot -Tpdf {parse_tree_dot} -o {parse_tree_file}')
            os.system(f'dot -Tpdf {parser_model_dot} -o {view_file}')
            # Cleanup unneeded dot files, we just use the PDFs for now
            parse_tree_dot.unlink(missing_ok=True)
            parser_model_dot.unlink(missing_ok=True)
            peg_tree_dot.unlink(missing_ok=True)
            peg_model_dot.unlink(missing_ok=True)
        # Return the refined model data, checking sequence length
        metadata = result.results.get('metadata')  # Optional section
        domain = result.results.get('domain_header')
        # lifecycle = result.results.get('lifecycle')
        # assigner = result.results.get('assigner')
        # events = result.results.get('events')
        # states = result.results.get('state_block')
        # You can draw classes without rels, but not the other way around!
        return Collaboration(
            domain=domain, actors=None, interactions=None, metadata=None if not metadata else metadata[0]
        )

if __name__ == "__main__":
    markup_path = Path(__file__).parent.parent / 'Test/int.ccv'
    x = CollabParser(view_file_path=markup_path, debug=True)
    x.parse()