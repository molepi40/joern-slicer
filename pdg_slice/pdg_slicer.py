from .type import *
from .cpg import CPGEdge, CPGNode, CPG
from .pdg import PDGEdge, PDGNode, PDG
from .find_target import find_target_nodes_by_lines, find_target_nodes_by_locations
from .output import map_node_to_src, output_source
import queue

"""

Slicer based on PDG and CPG exported  from joern.
You can use the slicer by calling pipeline method in this file.
"""


def _find_method_node(cpg_obj: CPG, call_node: CPGNode) -> CPGNode:
    """find corresponding method node of callsite
    """

    method_node = cpg_obj.get_method_node(call_node.get_attr(CPGPropertyType.METHOD_FULL_NAME))

    return method_node


def _find_param_node(cpg_obj: CPG, method_node: CPGNode, arg_node: CPGNode) -> CPGNode:
    """find corresponding parameter node of mehtod
    """

    for ast_edge in method_node.get_out_edge_iterator(CPGEdgeType.AST):

        # logically the ast_edge must exsit
        ast_dst_node = cpg_obj.get_node(ast_edge.get_dst())
        if ast_dst_node.get_label() == CPGNodeType.METHOD_PARAMETER_IN and \
           arg_node.get_attr(CPGPropertyType.ARGUMENT_INDEX) == ast_dst_node.get_attr(CPGPropertyType.INDEX):
            return ast_dst_node


def _add_call_dependency(cpg_obj: CPG, pdg_obj: PDG, call_node: CPGNode):
    """add method -> call dependency
    """

    method_node = _find_method_node(cpg_obj, call_node)
    if method_node.get_attr(CPGPropertyType.IS_EXTERNAL) == "true":
        return

    if not pdg_obj.have_node(method_node.get_id()):
        pdg_obj.add_pdg_node(method_node.get_id(), method_node.get_label().name)
    pdg_obj.add_pdg_edge(call_node.get_id(), method_node.get_id(), PDGEdgeType.DDG)


def _add_arg_dependency(cpg_obj: CPG, pdg_obj: PDG, arg_node: CPGNode):
    """add argument -> parameter dependency
    """

    for arg_edge in arg_node.get_in_edge_iterator(CPGEdgeType.ARGUMENT):

        call_node = cpg_obj.get_node(arg_edge.get_src())
        if call_node.get_label() != CPGNodeType.CALL:
            continue

        # exclude external method
        method_node = _find_method_node(cpg_obj, call_node)
        if method_node.get_attr(CPGPropertyType.IS_EXTERNAL) == "true":
            continue

        param_node = _find_param_node(cpg_obj, method_node, arg_node)
        if not pdg_obj.have_node(arg_node.get_id()):
            pdg_obj.add_pdg_node(arg_node.get_id(), arg_node.get_label().name)
            pdg_obj.add_pdg_edge(arg_node.get_id(), param_node.get_id(), PDGEdgeType.CDG)


def add_dependency(cpg_obj: CPG, pdg_obj: PDG) -> None:
    """add dependency edge in PDG

    callsite and cerresponding method \n
    callsite arguments and corresponding method parameter
    """

    for cpg_node in cpg_obj.get_nodes_iterator():

        # argument of call
        if cpg_node.get_in_edge_list(CPGEdgeType.ARGUMENT):
            _add_arg_dependency(cpg_obj, pdg_obj, cpg_node)
        
        # call
        if cpg_node.get_label() == CPGNodeType.CALL:
            _add_call_dependency(cpg_obj, pdg_obj, cpg_node)


def _traverse(cpg_obj: CPG, pdg_obj: PDG, target_nodes: list[CPGNode], is_forward: bool) -> set[CPGNode]:
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
            if not pdg_obj.have_node(node_id):
                continue
            pdg_node = pdg_obj.get_node(node_id)


            # collect out edge of the node
            for out_edge in pdg_node.get_out_edge_iterator():
                next_node_id = out_edge.get_dst()
                if next_node_id in visit:
                    continue
                next_node = cpg_obj.get_node(next_node_id)
                work_list.put(next_node)

    else:

        # backward  traversal
        while not work_list.empty():

            # take a node from work list
            cpg_node = work_list.get()
            # print(f"get node {cpg_node.get_id()} {cpg_node.get_label()}")
            node_id = cpg_node.get_id()
            if node_id in visit:
                continue
            visit.add(node_id)
            node_collection.add(cpg_node)
            if not pdg_obj.have_node(node_id):
                continue
            pdg_node = pdg_obj.get_node(node_id)

            # collect in edge of the node
            for in_edge in pdg_node.get_in_edge_iterator():
                next_node_id = in_edge.get_src()
                if next_node_id in visit:
                    continue
                next_node = cpg_obj.get_node(next_node_id)
                work_list.put(next_node)

    return node_collection


def _find_dependency(cpg_obj: CPG, pdg_obj: PDG, criterion: dict[str, set[tuple]]):
    """ find nodes on which selected nodes are dependent by backwardly traverse PDG
    """

    # find target node in cpg
    for file in criterion:
        if type(criterion[file]) == list:
            target_nodes = find_target_nodes_by_lines(cpg_obj, criterion)
        else:
            target_nodes = find_target_nodes_by_locations(cpg_obj, criterion)
        break
    dependency = _traverse(cpg_obj, pdg_obj, target_nodes, False)

    return dependency


def preprocess(cpg_dir: str, pdg_dir: str, add_dp) -> tuple[CPG, PDG]:
    """ load graph and add dependency
    """
    
    cpg_obj = CPG()
    cpg_obj.load_from_dot(cpg_dir)
    pdg_obj = PDG()
    pdg_obj.load_from_dot(pdg_dir)

    if add_dp:
        add_dependency(cpg_obj, pdg_obj)
    
    return cpg_obj, pdg_obj


def run_slice(cpg_obj: CPG, pdg_obj: PDG, src_dir, criterion: dict[str, list| set], output_file: str):
    """ run slice on PDG and output slices
    """

    dependency_nodes = _find_dependency(cpg_obj, pdg_obj, criterion)
    dependency_src = map_node_to_src(dependency_nodes)
    output_source(src_dir, dependency_src, output_file)    


def pipeline(cpg_dir:str, pdg_dir:str, src_dir: str, criterion: list[dict[str, set[tuple]]], output_file: str, add_dp):
    """pipeline of this dependency slicer
    """

    cpg_obj, pdg_obj = preprocess(cpg_dir, pdg_dir, add_dp)

    run_slice(cpg_obj, pdg_obj, src_dir, criterion, output_file)