""" layout_visitor.py """
from arpeggio import PTNodeVisitor
from flatland.datatypes.connection_types import NodeFace
from flatland.flatland_exceptions import ConflictingGraftFloat, MultipleGraftsInSameBranch, ExternalLocalGraftConflict
from flatland.flatland_exceptions import MultipleFloatsInSameBranch, TrunkLeafGraftConflict, GraftRutBranchConflict
from flatland.flatland_exceptions import ExternalGraftOnLastBranch

face_map = {'r': NodeFace.RIGHT, 'l': NodeFace.LEFT, 't': NodeFace.TOP, 'b': NodeFace.BOTTOM}

class LayoutVisitor(PTNodeVisitor):
    """
    Organized in the same categories commented in the clean peg grammar file.

        Some conventions:

        - Comment each visit with parsing semantics
        - Descriptive named variables if processing is required
        - Use *node.rule_name* in case the rule name changes
        - Combine values into dictionaries for stability, ease of interpretation and to avoid mistakes
        - Assigining result to a variable that is returned for ease of debugging
    """

    # Elements
    def visit_space(self, node, children):
        """Discard spaces"""
        return None

    def visit_number(self, node, children):
        """Natural number"""
        return int(node.value)

    def visit_name(self, node, children):
        """Words and delmiters joined to form a complete name"""
        name = ''.join(children)
        return name

    def visit_duplicate(self, node, children):
        """Repeated node number"""
        return {node.rule_name: int(children[0]) }

    def visit_wrap(self, node, children):
        """Number of lines to wrap"""
        return {node.rule_name: int(children[0]) }

    # Diagram
    def visit_diagram(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_padding(self, node, children):
        """Keyword argument"""
        d = dict(zip(['left', 'bottom', 'top', 'right'], children))
        return d

    def visit_frame(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_frame_presentation(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_notation(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_presentation(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_sheet(self, node, children):
        """Keyword argument"""
        return children[0]

    def visit_orientation(self, node, children):
        """Keyword argument"""
        return children[0]

    # Face attachment
    def visit_node_ref(self, node, children):
        """name number?"""
        return children


    def visit_face(self, node, children):
        """Face character"""
        return face_map[node.value]

    def visit_dir(self, node, children):
        """Pos-neg direction"""
        return 1 if node.value == '+' else -1

    def visit_anchor(self, node, children):
        """Anchor position"""
        anchor = 'float' if children[0] == '*' else children[0]
        return anchor

    def visit_node_face(self, node, children):
        """Where connector attaches to node face"""
        nface = {k:v[0] for k,v in children.results.items()}
        return nface

    # Alignment
    def visit_notch(self, node, children):
        """The digit 0 or a positive or negative number of notches"""
        if children[0] == '0':
            return 0
        else:
            scale = -1 if children[0] == '-' else 1
            return int(children[1]) * scale

    def visit_valign(self, node, children):
        """Vertical alignment of noce in its cell"""
        return {node.rule_name: children[0].upper()}

    def visit_halign(self, node, children):
        """Horizontal alignment of noce in its cell"""
        return {node.rule_name: children[0].upper()}

    def visit_node_align(self, node, children):
        """Vertical and/or horizontal alignment of node in its cell"""
        if len(children) == 2:
            # Merge the two dictionaries
            return {**children[0], **children[1]}
        else:
            return children[0]

    def visit_path(self, node, children):
        """Lane and rut followed by a connector bend"""
        # Rut is zero by default
        path = {node.rule_name: {'lane': children[0], 'rut': children.results.get('notch', [0])[0]} }
        return path  # { path: { lane: <lane_num>, rut: <rut_displacement> }

    # Node
    def visit_node_loc(self, node, children):
        """row_span col_span"""
        return {node.rule_name: children}

    def visit_span(self, node, children):
        """number number?"""
        return children

    def visit_node_name(self, node, children):
        """name number?"""
        return {node.rule_name: ''.join(children)}

    def visit_grid_place(self, node, children):
        """node_loc node_align?"""
        d = {k: v for c in children for k, v in c.items()}
        return d

    def visit_node_placement(self, node, children):
        """grid_place+"""
        return {'placements': children}

    def visit_node_spec(self, node, children):
        """node_name wrap? node_placement"""
        ditems = {k: v for c in children for k, v in c.items()}
        return ditems

    def visit_node_block(self, node, children):
        """All node placements"""
        return children

    # Binary connector
    def visit_tertiary_node(self, node, children):
        """Tertiary node face and anchor"""
        return {node.rule_name: children[0]}

    def visit_sname_place(self, node, children):
        """Side of stem axis and number of lines in text block"""
        d = {'stem_dir': children[0]}  # initialize d
        d.update(children[1]) # Add wrap key
        return d

    def visit_bend(self, node, children):
        """Number of bend where cname appears"""
        return {node.rule_name: int(children[0])}

    def visit_tstem(self, node, children):
        """T stem layout info"""
        items = {k: v for d in children for k, v in d.items()}
        items['anchor'] = items.get('anchor', 0)
        tstem = {node.rule_name: items}
        return tstem

    def visit_pstem(self, node, children):
        """P stem layout info"""
        items = {k: v for d in children for k, v in d.items()}
        items['anchor'] = items.get('anchor', 0)
        pstem = {node.rule_name: items}
        return pstem

    def visit_paths(self, node, children):
        """A sequence of one or more paths since a binary connector may bend multiple times"""
        paths = { node.rule_name : [p['path'] for p in children] }
        return paths

    def visit_binary_layout(self, node, children):
        """All layout info for the binary connector"""
        # Combine all child dictionaries
        items = {k: v for d in children for k, v in d.items()}
        return items

    # Tree connector
    def visit_trunk_face(self, node, children):
        """A single trunk node at the top of the tree layout. It may or may not graft its branch."""
        face = children[0]  # Face, node and optional notch
        graft = False if len(children) == 1 else True
        if 'anchor' not in face.keys():
            face['anchor'] = 0  # A Trunk face is never grafted, so an unspecified anchor is 0
        tface = { 'trunk_face': { 'node_ref': face.pop('node_ref'), **face, 'graft': graft } }
        return tface

    def visit_leaf_face(self, node, children):
        """Branch face that may be a graft to its branch (local) or the (next) branch"""
        lface = children[0]
        graft = None
        if 'anchor' not in lface.keys():
            lface['anchor'] = 0  # If not float or a number, it must be zero in a tree layout
        if len(children) == 2:
            graft = 'local' if children[1] == '>' else 'next'
        if lface['anchor'] == 'float' and graft:
            raise ConflictingGraftFloat(stem=lface['name'])
        lface['graft'] = graft
        node_ref = lface.pop('node_ref')
        name = node_ref[0] if len(node_ref) == 1 else f"{node_ref[0]}_{node_ref[1]}"
        return { name: lface }  # Single element dictionary indexed by the node name

    def visit_leaf_faces(self, node, children):
        """Combine into dictionary of each leaf face indexed by node name"""
        lfaces = {k: v for d in children for k, v in d.items()}
        if len([lfaces[n]['graft'] for n in lfaces if lfaces[n]['graft']]) > 1:
            raise MultipleGraftsInSameBranch(branch=set(lfaces.keys()))
        if len([lfaces[n]['anchor'] for n in lfaces if lfaces[n]['anchor'] == 'float']) > 1:
            raise MultipleFloatsInSameBranch(branch=set(lfaces.keys()))
        return { node.rule_name: lfaces }

    def visit_branch(self, node, children):
        """A tree connector branch"""
        branch = {k: v for d in children for k, v in d.items()}
        # Verify that this is either an interpolated, rut or graft branch and not an illegal mix
        # If a path is specified it is a rut branch or if there is a local graft it is a grafted branch
        # If both path and local graft are present in the same branch it is illegal
        if branch.get('path', None):  # Path specified, so there should be no local grafts in this branch
            lf = branch['leaf_faces']
            local_graft = [lf[n]['graft'] for n in lf if lf[n]['graft'] == 'local']
            if local_graft:
                raise GraftRutBranchConflict(branch=set(lf.keys()))
        # Return dictionary of leaf faces and an optional path keyed to the local rule
        return { node.rule_name: branch }

    def visit_tree_layout(self, node, children):
        """All layout info for the tree connector"""
        tlayout = children[0]
        # If the trunk is grafting (>), there can be no other leaf stem grafting locally (>)
        tlayout['branches'] = [c['branch'] for c in children[1:]]
        tgraft = tlayout['trunk_face']['graft']
        tleaves = tlayout['branches'][0]['leaf_faces']
        if tgraft and [tleaves[n]['graft'] for n in tleaves if tleaves[n]['graft'] == 'local']:
            raise TrunkLeafGraftConflict()  # In the first branch (trunk branch) both trunk and some leaf are grafting
        # For all offshoot (non-trunk) branches, there can be no local graft (>) if the preceding branch
        # is grafting externally (>>).  In other words, no more than one graft per branch.
        for b, next_b in zip(tlayout['branches'], tlayout['branches'][1:]):
            lf = b['leaf_faces']
            external_graft = [lf[n]['graft'] for n in lf if lf[n]['graft'] == 'next']
            if external_graft:
                next_lf = next_b['leaf_faces']
                if [next_lf[n]['graft'] for n in next_lf if next_lf[n]['graft'] == 'local']:
                    # External graft conflicts with local branch
                    raise ExternalLocalGraftConflict(set(lf.keys()))
        # Check for dangling external graft in last branch
        last_lf = tlayout['branches'][-1]['leaf_faces']
        external_graft = [last_lf[n]['graft'] for n in last_lf if last_lf[n]['graft'] == 'next']
        if external_graft:
            raise ExternalGraftOnLastBranch(branch=set(last_lf.keys()))
        return tlayout

    # Connector
    def visit_cname_place(self, node, children):
        """Name of connector and the side of the connector axis where it is placed"""
        cplace = {'cname': children.results['name'][0], 'dir': children.results.get('dir', [1])[0]}
        return cplace

    def visit_connector_layout(self, node, children):
        """All layout info for the connector"""
        # Combine all child dictionaries
        items = {k: v for d in children for k, v in d.items()}
        items['bend'] = items.get('bend', 1)  # No bend supplied, assume 1
        return items

    def visit_connector_block(self, node, children):
        return children

    def visit_layout_spec(self, node, children):
        return children.results

    # Root
    def visit_diagram_layout(self, node, children):
        return children