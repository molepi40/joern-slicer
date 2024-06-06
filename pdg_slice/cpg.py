import pydot
import os
import re
from .type import *
from collections.abc import Generator


""" CPG module

This module contains classes associated with CPG(code property graph).
These classes are CPGEdge, CPGNode, CPG. You can use them to load CPG from a dot file.

example:
    cpg = CPG()
    cpg.load_from_dot("./cpg")

"""


class CPGEdge:
    """class for CPG edge

    Directed edge <src, dst>. \n
    label is the type of the edge. \n
    head_next is the next edge of source node's out edge. \n
    tail_next is the next edge of destination node's in edge.

    """

    def __init__(self, edge) -> None:
        if type(edge) == tuple:
            self.src, self.dst, self.label = edge
        else:
            self.src = int(edge.get_source())
            self.dst = int(edge.get_destination())
            self.label: CPGEdgeType = CPGEdgeType[edge.get_attributes()["label"]]

        self.head_next: CPGEdge = None
        self.tail_next: CPGEdge = None
    
    def set_head_next(self, edge):
        self.head_next = edge
    
    def set_tail_next(self, edge):
        self.tail_next = edge
    
    def get_src(self):
        return self.src
    
    def get_dst(self):
        return self.dst
    
    def get_label(self):
        return self.label
    
    def get_head_next(self):
        return self.head_next
    
    def get_tail_next(self):
        return self.tail_next
    

class CPGNode:
    """class for CPG node

    id is the name of the node. \n
    label is the type of the node. \n
    If a node contains code in source file, its line_number is the start line of the code. \n
    in_edge_list and out_edge_list are part of the orthogonal linked list which depicts the graph.

    """

    def __init__(self, dot_node, in_method: str = None, in_file: str = None) -> None:

        # id
        self.id = int(dot_node.get_name())
        
        # attributes
        attrs: dict[str] = dot_node.get_attributes()
        self.label = CPGNodeType[attrs["label"]]
        del attrs["label"]
        self.attrs = {CPGPropertyType[key]: value for key, value in attrs.items()}                      
        
        # edge
        self.in_edge_list: dict[CPGEdgeType, CPGEdge] = dict()
        self.out_edge_list: dict[CPGEdgeType, CPGEdge] = dict()
        CPGNode._initialize_edge_list(self.in_edge_list)
        CPGNode._initialize_edge_list(self.out_edge_list)
        
        # file and method
        self.in_file = in_file
        self.in_method = in_method
    
    def _initialize_edge_list(edge_list: dict[CPGEdgeType, CPGEdge]) -> None:
        for edge_type in CPGEdgeType:
            edge_list[edge_type] = None
    
    def add_in_edge(self, edge: CPGEdge) -> None:
        if edge.get_label() in self.in_edge_list:
            edge.set_tail_next(self.in_edge_list[edge.get_label()])
        self.in_edge_list[edge.get_label()] = edge
    
    def add_out_edge(self, edge: CPGEdge) -> None:
        if edge.get_label() in self.out_edge_list:
            edge.set_head_next(self.out_edge_list[edge.get_label()])
        self.out_edge_list[edge.get_label()] = edge
    
    def have_attr(self, attr_key: CPGPropertyType) -> bool:
        return attr_key in self.attrs    

    def get_id(self) -> int:
        return self.id

    def get_label(self) -> CPGNodeType:
        return self.label
    
    def get_attr(self, attr_key: CPGPropertyType):
        return self.attrs[attr_key]

    def get_in_method(self) -> str:
        return self.in_method

    def get_in_file(self) -> str:
        return self.in_file
    
    def get_in_edge_list(self, edge_type: CPGEdgeType) -> CPGEdge:
        return self.in_edge_list[edge_type]

    def get_out_edge_list(self, edge_type: CPGEdgeType) -> CPGEdge:
        return self.out_edge_list[edge_type]

    def get_in_edge_iterator(self, edge_type: CPGEdgeType) -> Generator[CPGEdge, None, None]:
        cur = self.in_edge_list[edge_type]
        while cur:
            yield cur
            cur = cur.get_tail_next()
    
    def get_out_edge_iterator(self, edge_type: CPGEdgeType) -> Generator[CPGEdge, None, None]:
        cur = self.out_edge_list[edge_type]
        while cur:
            yield cur
            cur = cur.get_head_next()


class CPG:
    """class for CPG
    
    nodes is the collection of all CPG nodes

    """
    
    def __init__(self) -> None:
        
        # node collection for the whole program
        self.nodes: dict[int, CPGNode] = dict()

        # method collection
        self.methods: dict[str, CPGNode] = dict()

        # type declaration collection
        self.type_decls: dict[str, CPGNode] = dict()
    
    def load_from_dot(self, cpg_dir):

        # directory of cpgs of every file
        for file_name in os.listdir(cpg_dir):

            file_dir = os.path.join(cpg_dir, file_name)
            global_dot_file = None

            # method cpg
            for method_name_dot in os.listdir(file_dir):

                # handle global dot file at last. now put it aside.
                if method_name_dot == "_global_.dot":
                    global_dot_file = os.path.join(file_dir, method_name_dot)
                    continue

                # load cpg
                method_name = CPG._parse_file_dot(method_name_dot)
                method_dot_file = os.path.join(file_dir, method_name_dot)
                graph = pydot.graph_from_dot_file(method_dot_file)[0]
                
                # add nodes of cpg
                for dot_node in graph.get_node_list():
                    node = CPGNode(dot_node, method_name, file_name)
                    self.nodes[node.get_id()] = node

                    if node.get_label() == CPGNodeType.METHOD:
                        self.methods[node.get_attr(CPGPropertyType.FULL_NAME)] = node

                    if node.get_label() == CPGNodeType.TYPE_DECL:
                        self.type_decls[node.get_attr(CPGPropertyType.FULL_NAME)] = node
                
                # add edges of cpg
                for dot_edge in graph.get_edge_list():
                    edge = CPGEdge(dot_edge)
                    self.nodes[edge.get_src()].add_out_edge(edge)
                    self.nodes[edge.get_dst()].add_in_edge(edge)
            
            # if there is a global dot file
            if global_dot_file:
                graph = pydot.graph_from_dot_file(global_dot_file)[0]
                for dot_node in graph.get_node_list():
                    node_id = int(dot_node.get_name())
                    if node_id not in self.nodes:
                        node = CPGNode(dot_node, "_global_", file_name)
                        self.nodes[node_id] = node
                for dot_edge in graph.get_edge_list():
                    src = int(dot_edge.get_source())
                    dst = int(dot_edge.get_destination())
                    if (self.nodes[src].get_in_method() != "_global_") and (self.nodes[dst].get_in_method() != "_global_"):
                        continue
                    edge = CPGEdge(dot_edge)                  
                    self.nodes[edge.get_src()].add_out_edge(edge)
                    self.nodes[edge.get_dst()].add_in_edge(edge)        
            
    def _parse_file_dot(file_name: str) -> str:
        return re.match(r"(?P<method>.+)\.dot", file_name).groupdict()["method"]

    def get_nodes_iterator(self) -> Generator[CPGNode]:
        for node in self.nodes.values():
            yield node
    
    def get_node(self, node_id: int) -> CPGNode:
        return self.nodes[node_id]
    
    def get_method_node(self, method_full_name: str) -> CPGNode:
        return self.methods[method_full_name]
    
    def get_type_decl_node(self, type_full_name: str) -> CPGNode:
        if type_full_name in self.type_decls:
            return self.type_decls[type_full_name]
        else:
            return None


def test():
    cpg = CPG("./class-cpg")
    cpg.get_node(67)

if __name__ == "__main__":
    test()
