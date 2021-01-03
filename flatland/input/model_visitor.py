""" model_visitor.py """

from arpeggio import PTNodeVisitor

class SubsystemVisitor(PTNodeVisitor):

    def visit_nl(self, node, children):
        return None

    def visit_sp(self, node, children):
        return None

    def visit_mult(self, node, children):
        """Binary association (not association class) multiplicity"""
        mult = node.value  # No children because literal 1 or M is thrown out
        return mult

    def visit_acword(self, node, children):
        """All caps word"""
        return node.value  # No children since this is a literal

    def visit_icaps_name(self, node, children):
        """Model element name"""
        name = ''.join(children)
        return name

    def visit_class_header(self, node, children):
        """Beginning of class section, includes name"""
        abbr = None if len(children) == 1 else children[1]
        return {'name': children[0], "abbr": abbr}

    def visit_subsystem_header(self, node, children):
        """Beginning of sybsystem section"""
        abbr = None if len(children) == 1 else children[1]
        return {'subsys_name': children[0], 'abbr': abbr}

    def visit_body_line(self, node, children):
        """Lines that we don't need to parse yet, but eventually will"""
        # TODO: These should be attributes and actions
        body_text_line = children[0]
        return body_text_line

    def visit_phrase(self, node, children):
        """Phrase on one side of a binary relationship phrase"""
        phrase = ''.join(children)
        return phrase

    def visit_assoc_class(self, node, children):
        """Association class name and multiplicity"""
        return { "assoc_mult": children[0], "assoc_cname": children[1] }

    def visit_t_side(self, node, children):
        """T side of a binary association"""
        return {node.rule_name: {"phrase": children[0], "mult": children[1], "cname": children[2]}}

    def visit_p_side(self, node, children):
        """P side of a binary association"""
        return {node.rule_name: {"phrase": children[0], "mult": children[1], "cname": children[2]}}

    def visit_rname(self, node, children):
        """The Rnum on any relationship"""
        return {"rnum": children[0]}

    def visit_superclass(self, node, children):
        """Superclass in a generalization relationship"""
        return children[0]

    def visit_subclass(self, node, children):
        """Subclass in a generalization relationship"""
        return children[0]

    def visit_gen_rel(self, node, children):
        """Generalization relationship"""
        return {"superclass": children[0], "subclasses": children[1:]}

    def visit_binary_rel(self, node, children):
        """Binary relationship with or without an association class"""
        items = {k: v for d in children for k, v in d.items()}
        return items

    def visit_rel(self, node, children):
        """Relationship rnum and rel data"""
        return {**children[0], **children[1]}

    def visit_method_block(self, node, children):
        """Methods (unparsed)"""
        # TODO: Parse these eventually
        return children  # truncate newline terminator

    def visit_attr_block(self, node, children):
        """Attribute text (unparsed)"""
        # TODO: Parse these eventually
        return {"attributes": children}

    def visit_class_set(self, node, children):
        """All of the classes"""
        return children

    def visit_class_block(self, node, children):
        """A complete class with attributes, methods, state model"""
        # TODO: No state models yet
        return {**children[0], **children[1]}

    def visit_rel_section(self, node, children):
        """Relationships section with all of the relationships"""
        return children

    def visit_subsystem(self, node, children):
        """The complete subsystem"""
        return children


