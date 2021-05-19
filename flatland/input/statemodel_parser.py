""" statemodel_parser.py – First attempt to parse class block """

from flatland.flatland_exceptions import ModelGrammarFileOpen, ModelInputFileOpen, ModelInputFileEmpty
from flatland.flatland_exceptions import ModelParseError
from flatland.input.statemodel_visitor import StateModelVisitor
from arpeggio import visit_parse_tree, NoMatch
from arpeggio.cleanpeg import ParserPEG
from collections import namedtuple
from flatland.input.nocomment import nocomment
import os
from pathlib import Path

StateModel = namedtuple('State_model', 'metadata domain lifecycle assigner events states')

class StateModelParser:
    """
    Parses an Executable UML state model input file using the arpeggio parser generator

        Attributes

        - grammar_file -- (class based) Name of the system file defining the Executable UML grammar
        - root_rule_name -- (class based) Name of the top level grammar element found in grammar file
        - debug -- debug flag (used to set arpeggio parser mode)
        - model_grammar -- The model grammar text read from the system grammar file
        - model_text -- The input model text read from the user supplied text file
    """
    grammar_file_name = "model_markup/statemodel.peg"
    grammar_file = Path(__file__).parent.parent / grammar_file_name
    root_rule_name = 'statemodel'  # We don't draw a diagram larger than a single subsystem
    xuml_model_dir = Path(__file__).parent.parent / "examples" / "elevator"

    def __init__(self, model_file_path, debug=True):
        """
        Constructor

        :param model_file_path:  Where to find the user supplied model input file
        :param debug:  Debug flag
        """
        self.debug = debug
        self.model_file_path = model_file_path

        # Read the grammar file
        try:
            self.model_grammar = nocomment(open(StateModelParser.grammar_file, 'r').read())
        except OSError as e:
            raise ModelGrammarFileOpen(StateModelParser.grammar_file)

        # Read the model file
        try:
            self.model_text = nocomment(open(self.model_file_path, 'r').read(), prefix='///')
        except OSError as e:
            raise ModelInputFileOpen(self.model_file_path)

        if not self.model_text:
            raise ModelInputFileEmpty(self.model_file_path)

    def parse(self) -> StateModel:
        """
        Parse the model file and return the content
        :return:  The abstract syntax tree content of interest
        """
        # Create an arpeggio parser for our model grammar that does not eliminate whitespace
        # We interpret newlines and indents in our grammar, so whitespace must be preserved
        parser = ParserPEG(self.model_grammar, StateModelParser.root_rule_name, skipws=False, debug=self.debug)
        # Now create an abstract syntax tree from our model text
        try:
            parse_tree = parser.parse(self.model_text)
        except NoMatch as e:
            raise ModelParseError(self.model_file_path.name, e) from None
        # Transform that into a result that is better organized with grammar artifacts filtered out
        result = visit_parse_tree(parse_tree, StateModelVisitor(debug=self.debug))
        # Make it even nicer using easy to reference named tuples
        if self.debug:
            # Transform dot files into pdfs
            peg_tree_dot = Path("peggrammar_parse_tree.dot")
            peg_model_dot = Path("peggrammar_parser_model.dot")
            parse_tree_dot = Path("statemodel_parse_tree.dot")
            parser_model_dot = Path("statemodel_peg_parser_model.dot")

            parse_tree_file = str(StateModelParser.xuml_model_dir / self.model_file_path.stem) + "_parse_tree.pdf"
            model_file = str(StateModelParser.xuml_model_dir / self.model_file_path.stem) + "_model.pdf"
            os.system(f'dot -Tpdf {parse_tree_dot} -o {parse_tree_file}')
            os.system(f'dot -Tpdf {parser_model_dot} -o {model_file}')
            # Cleanup unneeded dot files, we just use the PDFs for now
            parse_tree_dot.unlink(missing_ok=True)
            parser_model_dot.unlink(missing_ok=True)
            peg_tree_dot.unlink(missing_ok=True)
            peg_model_dot.unlink(missing_ok=True)
        # Return the refined model data, checking sequence length
        metadata = result.results.get('metadata')  # Optional section
        domain = result.results.get('domain_header')
        lifecycle = result.results.get('lifecycle')
        assigner = result.results.get('assigner')
        events = result.results.get('events')
        states = result.results.get('state_block')
        # You can draw classes without rels, but not the other way around!
        return StateModel(
            domain=domain, lifecycle=lifecycle, assigner=assigner,
            events={} if not events else events[0],
            states=states,
            metadata=None if not metadata else metadata[0]
        )

if __name__ == "__main__":
    markup_path = Path(__file__).parent.parent / 'Test/door.xsm'
    x = StateModelParser(model_file_path=markup_path, debug=True)
    x.parse()