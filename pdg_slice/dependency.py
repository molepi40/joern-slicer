from .cpg import *

"""

Add dependency edge on CPG.
"""


def _add_edge(src_node: CPGNode, dst_node: CPGNode, edge_type: CPGEdgeType):
    new_edgge = CPGEdge((src_node.get_id(), dst_node.get_id(), edge_type))
    src_node.add_out_edge(new_edgge)
    dst_node.add_in_edge(new_edgge)


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


def _add_call_dependency(cpg_obj: CPG, call_node: CPGNode):
    """add method -> call dependency
    """

    method_node = _find_method_node(cpg_obj, call_node)
    if method_node.get_attr(CPGPropertyType.IS_EXTERNAL) == "true":
        return

    _add_edge(call_node, method_node, CPGEdgeType.CALL_DP)


def _add_arg_dependency(cpg_obj: CPG, arg_node: CPGNode):
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
        _add_edge(arg_node, param_node, CPGEdgeType.PARAM_DP)


def _add_ref_dependency(cpg_obj: CPG, identifier_node: CPGNode):
    """add local -> identifier
    """
    
    for ref_edge in identifier_node.get_out_edge_iterator(CPGEdgeType.REF):
        dst_id = ref_edge.get_dst()
        local_node = cpg_obj.get_node(dst_id)
        _add_edge(local_node, identifier_node, CPGEdgeType.REF_DP)


def _add_type_decl_dependency(cpg_obj: CPG, local_node: CPGNode):
    """add type_decl -> local

    Type declaration will not output now.
    """

    type_name = local_node.get_attr(CPGPropertyType.TYPE_FULL_NAME)
    type_decl_node = cpg_obj.get_type_decl_node(type_name)

    if type_decl_node:
        _add_edge(type_decl_node, local_node, CPGEdgeType.TYPE_DP)


def _add_mem_dependency(cpg_obj: CPG, mem_node: CPGNode):
    """add type_decl -> member
    """

    for ast_edge in mem_node.get_in_edge_iterator(CPGEdgeType.AST):
        type_decl_node = cpg_obj.get_node(ast_edge.get_src())

        _add_edge(type_decl_node, mem_node, CPGEdgeType.MEM_DP)


def add_dependency(cpg_obj: CPG) -> None:
    """add dependency edge in CPG

    callsite and cerresponding method \n
    callsite arguments and corresponding method parameter \n
    reference to target \n
    type declaration \n
    membership
    """

    for cpg_node in cpg_obj.get_nodes_iterator():
        # call
        if cpg_node.get_label() == CPGNodeType.CALL:
            _add_call_dependency(cpg_obj, cpg_node)

        # argument of call
        if cpg_node.get_in_edge_list(CPGEdgeType.ARGUMENT):
            _add_arg_dependency(cpg_obj, cpg_node)
        
        # ref
        if cpg_node.get_out_edge_list(CPGEdgeType.REF):
            _add_ref_dependency(cpg_obj, cpg_node)
        
        # type decl
        if cpg_node.get_label() == CPGNodeType.LOCAL:
            _add_type_decl_dependency(cpg_obj, cpg_node)

        # member declaration
        if cpg_node.get_label() == CPGNodeType.MEMBER:  
            _add_type_decl_dependency(cpg_obj, cpg_node)
            _add_mem_dependency(cpg_obj, cpg_node)
        

        
        
