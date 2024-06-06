import queue
from .type import *
from .cpg import CPGEdge, CPGNode, CPG
from .dependency import add_dependency
from .output import map_node_to_src, output_source
from .find_target import find_target_nodes_by_lines, find_target_nodes_by_locations

"""
Slicer based on CPG, mainly its PDG player, and edges added according to program dependency.
You can use the slicer by calling pipeline method in this file.
"""


dependency_edge_type = [CPGEdgeType.CDG, CPGEdgeType.DDG,
                        CPGEdgeType.CALL_DP, CPGEdgeType.PARAM_DP,
                        CPGEdgeType.REF_DP,
                        CPGEdgeType.TYPE_DP, CPGEdgeType.MEM_DP]


def _add_forward_dependency_node(cpg_obj: CPG, src_node: CPGNode, work_list: queue.Queue[CPGNode], visit: set[int]) -> bool:

    for edge_type in dependency_edge_type:
        for edge in src_node.get_out_edge_iterator(edge_type):
            dst_id = edge.get_dst()
            if dst_id in visit:
                continue
            dst_node = cpg_obj.get_node(dst_id)
            work_list.put(dst_node)


def _add_backward_dependency_node(cpg_obj: CPG, dst_node: CPGNode, work_list: queue.Queue[CPGNode], visit: set[int]) -> bool:

    for edge_type in dependency_edge_type:
        for edge in dst_node.get_in_edge_iterator(edge_type):
            src_id = edge.get_src()              
            if src_id in visit:
                continue
            # print(src_id, dst_node.get_id(), edge.get_label().name)
            src_node = cpg_obj.get_node(src_id)
            work_list.put(src_node)


def _traverse(cpg_obj: CPG, target_nodes: list[CPGNode], is_forward: bool) -> set[CPGNode]:
    """traverse PDG to collect corresponding dependency nodes of target nodes forwardly or backwardly.
    """

    visit = set[int]()
    work_list = queue.Queue[CPGNode](0)
    node_collection = set[CPGNode]()

    for node in target_nodes:
        work_list.put(node)   
    
    # traversal on
    if is_forward:

        # forward traverssal
        while not work_list.empty():

            # take a node from work list 
            cpg_node = work_list.get()
            node_id = cpg_node.get_id()
            if node_id in visit:
                continue
            visit.add(node_id)
            node_collection.add(cpg_node)
            
            _add_forward_dependency_node(cpg_obj, cpg_node, work_list, visit)
    else:

        # backward  traversal
        while not work_list.empty():

            # take a node from work list
            cpg_node = work_list.get()
            node_id = cpg_node.get_id()
            if node_id in visit:
                continue
            visit.add(node_id)
            node_collection.add(cpg_node)

            _add_backward_dependency_node(cpg_obj, cpg_node, work_list, visit)

    return node_collection


def _find_dependency(cpg_obj: CPG, criterion: dict[str, list| set]) -> set[CPGNode]:
    """ find nodes on which selected nodes are dependent by backwardly traverse CPG
    """

    # find target node in cpg
    for file in criterion:
        if type(criterion[file]) == list:
            target_nodes = find_target_nodes_by_lines(cpg_obj, criterion)
        elif type(criterion[file]) == set:
            target_nodes = find_target_nodes_by_locations(cpg_obj, criterion)
        else:
            raise Exception("invaluable critera.")
        break

    dependencies = _traverse(cpg_obj, target_nodes, False)

    return dependencies


def preprocess(cpg_dir: str, pdg_dir: str, add_dp) -> CPG:
    """ load graph and add dependency
    """
    
    cpg_obj = CPG()
    cpg_obj.load_from_dot(cpg_dir)
    cpg_obj.add_pdg_edge_from_dot(pdg_dir)

    if add_dp:
        add_dependency(cpg_obj)
    
    return cpg_obj


def run_slice(cpg_obj: CPG, src_dir: str, criterion: dict[str, list| set], output_file: str):
    """ run slice on CPG and output slices
    """
    
    dependency_nodes = _find_dependency(cpg_obj, criterion)
    # for node in dependency_nodes:
    #     print(node.get_id(), " line: ",node.get_attr(CPGPropertyType.LINE_NUMBER))
    # print("\n")
    dependency_src = map_node_to_src(dependency_nodes)
    output_source(src_dir, dependency_src, output_file)  


def pipeline(cpg_dir:str, pdg_dir:str, src_dir: str, criterion: dict[str, list| set], output_file: str, add_dp):
    """pipeline of this dependency slicer
    """

    cpg_obj = preprocess(cpg_dir, pdg_dir, add_dp)

    run_slice(cpg_obj, src_dir, criterion, output_file, add_dp)