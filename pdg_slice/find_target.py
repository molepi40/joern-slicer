from .type import *
from .cpg import CPG, CPGNode


def find_target_nodes_by_locations(cpg_obj: CPG, locations: dict[str: set[tuple]]) -> list[CPGNode]:
    """find target CPG node according to locations
    """

    target_nodes = list[CPGNode]()
    for node in cpg_obj.get_nodes_iterator():
        file = node.get_in_file()
        if file in locations and \
           node.have_attr(CPGPropertyType.LINE_NUMBER) and \
           node.have_attr(CPGPropertyType.COLUMN_NUMBER) and \
           (int(node.get_attr(CPGPropertyType.LINE_NUMBER)), int(node.get_attr(CPGPropertyType.COLUMN_NUMBER))) in locations[file]:
            target_nodes.append(node)
    
    return target_nodes


def find_target_nodes_by_lines(cpg_obj: CPG, criteria: dict[str: list[int]]):
    """find target CPG node according to file name and line number, not considering node with more than one line
    """ 

    target_nodes = list[CPGNode]()
    for node in cpg_obj.get_nodes_iterator():
        file = node.get_in_file()
        if file in criteria and \
        node.have_attr(CPGPropertyType.LINE_NUMBER) and \
        (not node.have_attr(CPGPropertyType.LINE_NUMBER_END)) and \
        int(node.get_attr(CPGPropertyType.LINE_NUMBER)) in criteria[file]:
            target_nodes.append(node)

    return target_nodes
