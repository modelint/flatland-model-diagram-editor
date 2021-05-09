""" statemodel_visitor.py """

from arpeggio import PTNodeVisitor
from collections import namedtuple

# These named tuples help package up parsed data into meaningful chunks of state model content
StateBlock = namedtuple('StateBlock', 'name type creation_event activity transitions')
"""The model data describing a state including its activity, optional creation event and optional exit transitions"""
Parameter = namedtuple('Parameter', 'name type')
"""The name and data type of a parameter in a state model event signature"""
EventSpec = namedtuple('EventSpec', 'name type signature')
"""The name of an event, its type (normal or creation) and parameter signature"""

class StateModelVisitor(PTNodeVisitor):
    """Visit parsed units of an Executable UML State Model"""
    # Each header comment below corresponds to section in statemodel.peg file

    # Elements
    def visit_nl(self, node, children):
        """New line character"""
        return None

    def visit_sp(self, node, children):
        """Single space character"""
        return None

    def visit_acword(self, node, children):
        """All caps word"""
        return node.value  # No children since this is a literal

    def visit_icaps_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_sentence_name(self, node, children):
        """Used for event name"""
        name = ''.join(children)
        return name

    def visit_body_line(self, node, children):
        """Lines that we don't need to parse yet, but eventually will"""
        # TODO: These should be attributes and actions
        body_text_line = children[0]
        return body_text_line

    # State block
    def visit_deletion_state(self, node, children):
        """State with transition to deletion pseudo-state"""
        return {'state': children[0], 'type': 'deletion'}

    def visit_initial_state(self, node, children):
        """state_name [creation_event_name]: State entered via transition from initial pseudo-state"""
        s = children[0]
        e = None if len(children) < 2 else children[1]
        return { 'state': s,  'creation_event': e, 'type': 'creation' }

    def visit_normal_state(self, node, children):
        """State entered via normal (non-creation) event"""
        return {'state': children[0], 'type': 'normal'}

    def visit_state_name(self, node, children):
        """State name"""
        name = ''.join(children)
        return name

    def visit_transition(self, node, children):
        """event destination_state"""
        d = { 'transition': {'event': children[0]} }
        if len(children) > 1:
            d['transition'].update({'dest': children[1]})
        return children

    def visit_transitions(self, node, children):
        """All transitions exiting a state including any creation transitions"""
        return children

    def visit_activity(self, node, children):
        """Required state activity, which may or may not contain any actions"""
        return children

    def visit_state_header(self, node, children):
        """state_name"""
        return children[0]

    def visit_state_block(self, node, children):
        """All state data"""
        s = children[0]  # State info
        a = children[1]  # Activity (could be empty, but always provided)
        t = [] if len(children) < 3 else children[2]  # Optional transitions
        sblock = StateBlock(name=s['state'], creation_event=s.get('creation_event'),
                            type=s['type'], activity=a, transitions=t)
        return sblock

    # Events
    def visit_creation_event(self, node, children):
        """creation_event_name"""
        name = ''.join(children)
        return name, 'creation'

    def visit_normal_event(self, node, children):
        """normal_event_name"""
        name = ''.join(children)
        return name, 'normal'

    def visit_event_name(self, node, children):
        """All characters composing an event name"""
        name = ''.join(children)
        return name

    def visit_type_name(self, node, children):
        """All characters composing a data type name"""
        name = ''.join(children)
        return name

    def visit_param_name(self, node, children):
        """All characters composing a parameter name"""
        name = ''.join(children)
        return name

    def visit_parameter(self, node, children):
        """param_name type_name"""
        return Parameter(name=children[0], type=children[1])

    def visit_parameter_set(self, node, children):
        """list of { param_name: type_name } pairs"""
        return children

    def visit_signature(self, node, children):
        """Strips out parenthesis"""
        return children[0]

    def visit_event_spec(self, node, children):
        """event_name [signature]: Complete event specification including optional signature"""
        params = [] if len(children) < 2 else children[1]
        ename = children[0]  # name, type tuple
        espec = EventSpec(name=ename[0], type=ename[1], signature=params)
        return { ename[0]: espec }

    def visit_events(self, node, children):
        """All event specifications, creation and normal, defined for a state machine"""
        d = {k: v for e in children for k, v in e.items()}
        return d

    # Scope
    def visit_assigner(self, node, children):
        """Scope: If value supplied this is an assigner state model"""
        return {'rel': children[0] }

    def visit_lifecycle(self, node, children):
        """Scope: If value supplied this is a lifecycle state model"""
        return {'class': children[0] }

    def visit_domain_header(self, node, children):
        """domain_name"""
        name = children[0]
        return name

    # Metadata
    def visit_text_item(self, node, children):
        return children[0], False  # Item, Not a resource

    def visit_resource_item(self, node, children):
        return ''.join(children), True  # Item, Is a resource

    def visit_item_name(self, node, children):
        return ''.join(children)

    def visit_data_item(self, node, children):
        return { children[0]: children[1] }

    def visit_metadata(self, node, children):
        """Meta data section"""
        items = {k: v for c in children for k, v in c.items()}
        return items

    # Root
    def visit_statemodel(self, node, children):
        """The complete state machine (state model)"""
        return children
