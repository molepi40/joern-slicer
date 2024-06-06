from enum import Enum

"""type information of CPG and PDG
"""


class CPGEdgeType(Enum):
    """enum variable of CPGEdge type

    Specification could be seen in https://cpg.joern.io.

    """
    SOURCE_DILE = 0

    ALIAS_OF = 1
    BINDS_TO = 2
    INHERITS_FROM = 3

    AST = 4
    CONDITION = 5

    ARGUMENT = 6
    CALL = 7
    RECEIVER = 8

    CFG = 9

    DOMINATE = 10
    POST_DOMINATE = 11

    CDG = 12
    REACHING_DEF = 13
    PARAM_DP = 20
    CALL_DP = 21
    REF_DP = 22
    TYPE_DP = 23
    MEM_DP = 24

    CONTAINS = 14
    EVAL_TYPE = 15
    PARAMETER_LINK = 16

    TAGGED_BY = 17

    BINDS = 18
    
    REF = 19


class CPGNodeType(Enum):
    """enum variable of CPGNode type

    Specification could be seen in https://cpg.joern.io.

    """
    META_DATA = 0

    FILE = 1

    NAMESPACE = 2
    NAMESPACE_BLOCK = 3

    METHOD = 4
    METHOD_PARAMETER_IN = 5
    METHOD_PARAMETER_OUT = 6
    METHOD_RETURN = 7

    MEMBER = 8
    TYPE = 9
    TYPE_ARGUMENT = 10
    TYPE_DECL = 11
    TYPE_PARAMETER = 12

    AST_NODE = 13
    BLOCK = 14
    CALL = 15
    CALL_REPR = 16
    CONTROL_STRUCTURE = 17
    EXPRESSION = 18
    FIELD_IDENTIFIER = 19
    IDENTIFIER = 20
    JUMP_LABEL = 21
    JUMP_TARGET = 22
    LITERAL = 23
    LOCAL = 24
    METHOD_REF = 25
    MODIFIER = 26
    RETURN = 27
    TYPE_REF = 28
    UNKNOWN = 29

    CFG_NODE = 30

    COMMENT = 31

    FINDING = 32
    KEY_VALUE_PAIR = 33

    LOCATION = 34
    TAG = 35
    TAG_NODE_PAIR = 36

    CONFIG_FILE = 37

    BINDING = 38

    ANNOTATION = 39
    ANNOTATION_LITERAL = 40
    ANNOTATION_PARAMETER = 41
    ANNOTATION_PARAMETER_ASSIGN = 42
    ARRAY_INITIALIZER = 43

    DECLARATION = 44


class CPGPropertyType(Enum):
    """property of CPGNode

    Specification could be seen in https://cpg.joern.io.

    """
    LANGUAGE = 0
    OVERLAYS = 1
    ROOT = 2

    COLUMN_NUMBER = 3
    COLUMN_NUMBER_END = 4
    FILENAME = 5
    LINE_NUMBER = 6
    LINE_NUMBER_END = 7

    IS_VARIADIC = 8
    SIGNATURE = 9

    ALIAS_TYPE_FULL_NAME = 10
    INHERITS_FROM_TYPE_FULL_NAME = 11
    TYPE_DECL_FULL_NAME = 12
    TYPE_FULL_NAME = 13

    CANONICAL_NAME = 14
    CONTROL_STRUCTURE_TYPE = 15
    MODIFIER_TYPE = 16
    ORDER = 17

    ARGUMENT_INDEX = 18
    ARGUMENT_NAME = 19
    DISPATCH_TYPE = 20
    EVALUATION_STRATEGY = 21
    METHOD_FULL_NAME = 22

    VARIABLE = 23

    KEY = 24

    CLASS_NAME = 25
    CLASS_SHORT_NAME = 26
    METHOD_SHORT_NAME = 27
    NODE_LABEL = 28
    PACKAGE_NAME = 29
    SYMBOL = 30

    AST_PARENT_FULL_NAME = 31
    AST_PARENT_TYPE = 32
    CODE = 33
    CONTENT = 34
    FULL_NAME = 35
    HASH = 36
    INDEX = 37
    IS_EXTERNAL = 38
    NAME = 39
    PARSER_TYPE_NAME = 40
    VALUE = 41
    VERSION = 42
    CONTAINED_REF = 43

class PDGEdgeType(Enum):
    DDG = 0
    CDG = 1
    