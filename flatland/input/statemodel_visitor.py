""" statemodel_visitor.py """

from arpeggio import PTNodeVisitor
from collections import namedtuple

StateBlock = namedtuple('StateBlock', 'name type creation_event activity transitions')
Parameter = namedtuple('Parameter', 'name type')
EventSpec = namedtuple('EventSpec', 'name type signature')

class StateModelVisitor(PTNodeVisitor):

    # Elements
    def visit_nl(self, node, children):
        return None

    def visit_sp(self, node, children):
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
        return {'state': children[0], 'type': 'deletion'}

    def visit_creation_state(self, node, children):
        s = children[0]
        e = None if len(children) < 2 else children[1]
        return { 'state': s,  'creation_event': e, 'type': 'creation' }

    def visit_normal_state(self, node, children):
        return {'state': children[0], 'type': 'normal'}

    def visit_state_name(self, node, children):
        name = ''.join(children)
        return name

    def visit_transition(self, node, children):
        d = { 'transition': {'event': children[0]} }
        if len(children) > 1:
            d['transition'].update({'dest': children[1]})
        return children

    def visit_transitions(self, node, children):
        return children

    def visit_activity(self, node, children):
        return children

    def visit_state_header(self, node, children):
        """state_name"""
        return children[0]

    def visit_state_block(self, node, children):
        s = children[0]  # State info
        a = children[1]  # Activity (could be empty, but always provided)
        t = [] if len(children) < 3 else children[2]  # Optional transitions
        sblock = StateBlock(name=s['state'], creation_event=s.get('creation_event'),
                            type=s['type'], activity=a, transitions=t)
        return sblock

    # Events
    def visit_creation_event(self, node, children):
        return children[0], 'creation'

    def visit_normal_event(self, node, children):
        return children[0], 'normal'

    def visit_event_name(self, node, children):
        name = ''.join(children)
        return name

    def visit_type_name(self, node, children):
        name = ''.join(children)
        return name

    def visit_param_name(self, node, children):
        name = ''.join(children)
        return name

    def visit_parameter(self, node, children):
        """param_name, type_name"""
        return Parameter(name=children[0], type=children[1])

    def visit_parameter_set(self, node, children):
        """list of { param_name: type_name } pairs"""
        return children

    def visit_signature(self, node, children):
        """Strips out parenthesis"""
        return children[0]

    def visit_event_spec(self, node, children):
        params = None if len(children) < 2 else children[1]
        ename = children[0]  # name, type tuple
        espec = EventSpec(name=ename[0], type=ename[1], signature=params)
        return espec

    def visit_events(self, node, children):
        return { node.rule_name: children }

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
        """The complete subsystem"""
        return children


