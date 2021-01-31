"""
flatland_exceptions.py – Flatland specific exceptions
"""

# Every flatland error should have the same format
# with a standard prefix and postfix defined here
pre = "\nFlatland: ["
post = "]"


class FlatlandException(Exception):
    pass

class FlatlandIOException(FlatlandException):
    pass

class FlatlandDBException(FlatlandException):
    pass


class FlatlandUserInputException(FlatlandException):
    pass


class UnknownSheetGroup(FlatlandDBException):
    pass

class NonSystemInitialLayer(FlatlandException):
    pass

class LayoutParseError(FlatlandUserInputException):
    def __init__(self, layout_file, e):
        self.layout_file = layout_file
        self.e = e

    def __str__(self):
        return f'{pre}Parse error in layout "{self.layout_file}" : {self.e}"{post}'

class ModelParseError(FlatlandUserInputException):
    def __init__(self, model_file, e):
        self.model_file = model_file
        self.e = e

    def __str__(self):
        return f'{pre}Parse error in model "{self.model_file}" : {self.e}"{post}'

class ConflictingGraftFloat(FlatlandUserInputException):
    def __init__(self, stem):
        self.stem = stem

    def __str__(self):
        return f'{pre}A floating anchor(*) may not graft (>, >>): "{self.stem}"{post}'

class MultipleGraftsInSameBranch(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}There may be at most one graft (>, >>) per branch: "{self.branch}"{post}'

class TrunkLeafGraftConflict(FlatlandUserInputException):
    def __str__(self):
        return f'{pre}Leaf may not graft locally (>) if Trunk is grafting (>) {post}'

class ExternalLocalGraftConflict(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}Branch has local (>) graft with conflicting external graft (>>) in preceding branch: "{self.branch}"{post}'

class ExternalGraftOnLastBranch(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}Last branch in tree layout has a superfluous external (>>) graft: "{self.branch}"{post}'

class GraftRutBranchConflict(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}A rut branch, with (: Ln[R+/-n]), may not include a local graft(>): "{self.branch}"{post}'

class NoFloatInStraightConnector(FlatlandUserInputException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{pre}Straight connector "{self.name}" has no floating anchor (*). Specify one.{post}'

class MultipleFloatsInSameStraightConnector(FlatlandUserInputException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{pre}Straight connector "{self.name}" has two floating anchors (*). Specify one.{post}'

class MultipleFloatsInSameBranch(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}There may be at most one floating anchor (*) per branch: "{self.branch}"{post}'

class MultipleFloatsInSameBranch(FlatlandUserInputException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}There may be at most one floating anchor (*) per branch: "{self.branch}"{post}'


class ModelInputFileOpen(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this model input file: "{self.path}"{post}'

class ModelInputFileEmpty(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}For some reason, nothing was read from the model input file: "{self.path}"{post}'

class ModelGrammarFileOpen(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this model grammar file: "{self.path}"{post}'

class LayoutGrammarFileOpen(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this layout grammar file: "{self.path}"{post}'

class LayoutFileEmpty(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}For some reason, nothing was read from the diagram layout file: "{self.path}"{post}'

class LayoutFileOpen(FlatlandIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this layout grammar file: "{self.path}"{post}'



class InvalidNameSide(FlatlandUserInputException):
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f'Invalid side: {self.side} should be either 1 or -1'


class InvalidBendNumber(FlatlandUserInputException):
    def __init__(self, bend, max_bend):
        self.bend = bend
        self.max_bend = max_bend

    def __str__(self):
        return f'Invalid bend: {self.bend} should be in range: 1..{self.max_bend} where max is number of corners + 1'


class InvalidOrientation(FlatlandUserInputException):
    def __init__(self, orientation):
        self.orientation = orientation

    def __str__(self):
        return f'Orientation must be portrait or landscape, got: [{self.orientation}]'


class BadRowSpan(FlatlandException):
    def __init__(self, low_row, high_row):
        self.low_row = low_row
        self.high_row = high_row

    def __str__(self):
        return f'Row span should be <low,high>, but: [<{self.low_row}, {self.high_row}> specified]'

class BadColSpan(FlatlandException):
    def __init__(self, low_col, high_col):
        self.low_col = low_col
        self.high_col = high_col

    def __str__(self):
        return f'Col span should be <low,high>, but: [<{self.low_col}, {self.high_col}> specified]'

class BadRowNumber(FlatlandException):
    def __init__(self, col_num):
        self.col_num = col_num

    def __str__(self):
        return f'Illegal Row number: [{col_num}]'


class BadColNumber(FlatlandException):
    def __init__(self, col_num):
        self.col_num = col_num

    def __str__(self):
        return f'Illegal Col number: [{col_num}]'


class UnsupportedConnectorType(FlatlandException):
    def __init__(self, connector_type_name, diagram_type_name):
        self.connector_type_name = connector_type_name
        self.diagram_type_name = diagram_type_name

    def __str__(self):
        return f'Connector Type: "{self.connector_type_name}" is not defined for Diagram Type: "{self.diagram_type_name}"'


class OutofDiagramBounds(FlatlandException):
    def __init__(self, object_type: str, x_value: float, y_value: float):
        self.object_type = object_type
        self.x_value = x_value
        self.y_value = y_value

    def __str__(self):
        return f'Object [{self.object_type}] outside of diagram bounds at x:{self.x_value}, y:{self.y_value}'


class UnsupportedNotation(FlatlandException):
    pass


class UnsupportedDiagramType(FlatlandException):
    pass


class NotationUnsupportedForDiagramType(FlatlandException):
    pass


class SheetWidthExceededFE(FlatlandException):
    pass


class SheetHeightExceededFE(FlatlandException):
    pass


class CellOccupiedFE(FlatlandException):
    pass


class UnsupportedNodeType(FlatlandException):
    def __init__(self, node_type_name, diagram_type_name):
        self.node_type_name = node_type_name
        self.diagram_type_name = diagram_type_name

    def __str__(self):
        return f'Node Type: {self.node_type_name} is not defined for Diagram Type: {self.diagram_type_name}'


class UnknownSheetSize(FlatlandException):
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    def __str__(self):
        return f'Sheet: {self.sheet_name} is not defined'


class CellOutofBounds:
    pass


class EmptyTitleCompartment(FlatlandException):
    pass


class BranchCannotBeInterpolated(FlatlandException):
    pass
