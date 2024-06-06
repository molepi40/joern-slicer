import os
import pydot
import html
import re
from .type import *

""" PDG module

example:
    pdg = PDG()
    pdg.load_from_dot("./pdg")

"""


class PDGEdge:
    def __init__(self, edge) -> None:
        if type(edge) == tuple:
            self.src, self.dst, self.type = edge
        else:
            self.src = int(PDGNode._parse_node_name(edge.get_source()))
            self.dst = int(PDGNode._parse_node_name(edge.get_destination()))
            label_type = PDGEdge._parse_edge_label(edge.get_attributes()["label"])
            self.type = PDGEdgeType[label_type]

        self.head_next = self.tail_next = None
    
    def _parse_edge_label(label) -> str:
        label = html.unescape(label)
        return re.match(r"\"(?P<type>\w+):(?P<code>.+)\"", label).groupdict()["type"]

    def set_head_next(self, edge) -> None:
        self.head_next = edge
    
    def set_tail_next(self, edge) -> None:
        self.tail_next = edge
    
    def get_src(self) -> int:
        return self.src

    def get_dst(self) -> int:
        return self.dst

    def get_head_next(self):
        return self.head_next
    
    def get_tail_next(self):
        return self.tail_next
    

class PDGNode:
    def __init__(self, node) -> None:
        if type(node) == tuple:
            self.id, self.type = node
        else:
            self.id = int(PDGNode._parse_node_name(node.get_name()))
            self.type = PDGNode._parse_node_type(node.get_attributes()["label"])

        self.out_edge_list: PDGEdge = None
        self.in_edge_list: PDGEdge = None

        self.edge_generator = None
    
    def _parse_node_name(name):
        return re.match(r"\"(?P<id>\d+)\"", name).groupdict()["id"]

    def _parse_node_type(label):
        label = html.unescape(label)
        # shortest match
        return re.match(r"<\((?P<type>.+?),.*", label).groupdict()["type"]
    
    def add_in_edge(self, edge: PDGEdge):
        if self.in_edge_list:
            edge.set_tail_next(self.in_edge_list)
        self.in_edge_list = edge
    
    def add_out_edge(self, edge: PDGEdge):
        if self.out_edge_list:
            edge.set_head_next(self.out_edge_list)
        self.out_edge_list = edge

    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_in_edge_list(self):
        return self.in_edge_list
    
    def get_out_edge_list(self):
        return self.out_edge_list
    
    def get_in_edge_iterator(self):
        cur = self.in_edge_list
        while cur:
            yield cur
            cur = cur.get_tail_next()
    
    def get_out_edge_iterator(self):
        cur = self.out_edge_list
        while cur:
            yield cur
            cur = cur.get_head_next()


class PDG:
    def __init__(self) -> None:
        # node collection of pdg nodes
        self.nodes: dict[int, PDGNode] = dict()
    
    def load_from_dot(self, pdg_dir):
        for pdg_file in os.listdir(pdg_dir):

            # load pdg
            pdg_file = os.path.join(pdg_dir, pdg_file)
            graph = pydot.graph_from_dot_file(pdg_file)[0]
            
            # add nodes of pdg
            for dot_node in graph.get_node_list():
                node = PDGNode(dot_node)
                self.nodes[node.get_id()] = node
            
            # add edges of pdg
            for dot_edge in graph.get_edge_list():
                edge = PDGEdge(dot_edge)
                self.nodes[edge.get_src()].add_out_edge(edge)
                self.nodes[edge.get_dst()].add_in_edge(edge)
   
    def _parse_graph_name(name):
        return re.match(r"\"(?P<name>.+)\"", name).groupdict()["name"]
    
    def add_pdg_edge(self, src_id: int, dst_id: int, type: PDGEdgeType):
        edge = PDGEdge((src_id, dst_id, type))
        self.nodes[src_id].add_out_edge(edge)
        self.nodes[dst_id].add_in_edge(edge)
    
    def add_pdg_node(self, node_id, node_type):
        self.nodes[node_id] = PDGNode((node_id, node_type))
    
    def have_node(self, node_id):
        return node_id in self.nodes

    def get_node(self, node_id: int):
        return self.nodes[node_id]