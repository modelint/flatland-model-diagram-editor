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

    def visit_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_body_line(self, node, children):
        """Lines that we don't need to parse yet, but eventually will"""
        # TODO: These should be attributes and actions
        body_text_line = children[0]
        return body_text_line

    # State block
    def visit_state_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_creation(self, node, children):
        return 'creation'

    def visit_deletion(self, node, children):
        return 'deletion'

    def visit_state_header(self, node, children):
        """
        There are four possible cases:
            state name only (normal state)
            state name (creation transition with no event)
            state name (creation transition with event)
            state name (deletion state)
        """
        s = children[0]  # State name
        t = 'normal' if len(children) == 1 else children[1]  # normal, creation or deletion
        e = None if len(children) < 3 else children[2]  # creation event, if any
        assert not e or ( e and t == 'creation'), f'Creation event supplied for non creation event [{e}]'
        d = { 'state': s,  'type': t }  # we always have these two
        if e:
            d.update({'creation_event': e})  # add optional creation event
        return d

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

    def visit_state_block(self, node, children):
        """All state data"""
        s = children[0]  # State info
        a = children[1]  # Activity (could be empty, but always provided)
        t = [] if len(children) < 3 else children[2]  # Optional transitions
        sblock = StateBlock(name=s['state'], creation_event=s.get('creation_event'),
                            type=s['type'], activity=a, transitions=t)
        return sblock

    # Events
    def visit_event_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_parameter_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_creation_event(self, node, children):
        """creation_event_name"""
        name = ''.join(children)
        return name, 'creation'

    def visit_normal_event(self, node, children):
        """normal_event_name"""
        name = ''.join(children)
        return name, 'normal'

    def visit_type_name(self, node, children):
        """All characters composing a data type name"""
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
