import os
import json
from argparse import ArgumentParser

'''
traverse graph of given data-flow.json and output lines in sources
> python3 slice.py -h
'''

# load graph from json
def load_graph(json_file):
    with open(json_file, "r") as f:
        data = f.read()
    data = json.loads(data)
    return data["nodes"], data["edges"]

# transfer to edges of list
def get_list_edges(edges, src, dst):
    list_edges = dict()
    for edge in edges:
        src_node = edge[src]
        if src_node not in list_edges.keys():
            list_edges[src_node] = []
        list_edges[src_node].append(edge[dst])
    return list_edges


def find_target_nodes_by_locations(nodes, locations: dict[str: set[tuple]]):
    """find target CPG node according to locations
    """

    target_nodes = list()
    for node in nodes:
        if "parentFile" in node:
            file = node["parentFile"]
            if file in locations and \
               "lineNumber" in node and \
               "columnNumber" in node and \
               (node["lineNumber"][0], node["lineNumber"][0]) in locations[file]:
                target_nodes.append(node)

    return target_nodes


def find_target_nodes_by_lines(nodes, criteria: dict[str: list[int]]):
    """find target CPG node according to file name and line number, not considering node with more than one line
    """ 

    target_nodes = list()
    for node in nodes:
        if "parentFile" in criteria:
            file = node["parentFile"]
            for line in node["lineNUmber"]:
                if line in criteria[file]:
                    target_nodes.append(node)
                    break

    return target_nodes

# traverse graph from node
def graph_traversal(edges, src, visit):
    if src in edges.keys():
        for dst in edges[src]:
            if dst not in visit:
                visit.add(dst)
                graph_traversal(edges, dst, visit)
    return

# load graph from data-flow.json and traverse the graph forward and backward from selected line
def handle_data_flow_json(json_file: str, criteria: dict[str, list| set]):
    # load graph
    nodes, edges = load_graph(json_file)

    # filter nodes
    for file in criteria:
        if type(criteria[file]) == list:
            target_nodes = find_target_nodes_by_lines(nodes, criteria)
        elif type(criteria[file]) == set:
            target_nodes = find_target_nodes_by_locations(nodes, criteria)
        else:
            raise Exception("inavaluable criteria.")
            
    # link list edge
    reverse_edges = get_list_edges(edges, "dst", "src")
    edges = get_list_edges(edges, "src", "dst")

    # forward traversal
    # visit_forward = set()
    # for node in target_nodes:
    #     visit_forward.add(node["id"])
    #     graph_traversal(edges, node["id"], visit_forward)
    
    # backward traversal
    visit_backward = set()
    for node in target_nodes:
        graph_traversal(reverse_edges, node["id"], visit_backward)
    
    # get lines associated to visited nodes
    lines = dict()
    for node in nodes:
        if node["id"] in visit_backward:
            if "parentFile" in node:
                parent_file = node["parentFile"]
                if parent_file not in lines.keys():
                    lines[parent_file] = set()
                for line in node["lineNumber"]:
                    lines[parent_file].add(line)
    
    # sort lines
    for key in lines.keys():
        lines[key] = sorted(list(lines[key]))

    return lines

# output lines in single source file
def output_srcfile_lines(src_dir: str, output_file: str, lines: dict):
    
    output_file = open(output_file, "w")

    for file_base in os.listdir(src_dir):
        file = os.path.join(src_dir, file_base)
        if file_base in lines.keys():
            output_file.write(file_base + "\n```\n")
            with open(file, "r") as f:
                src = f.readlines()
            for line in lines[file_base]:
                output_file.write(str(line) + src[line - 1])
            output_file.write("```\n")


# pipeline to output lines in source files according to data-flow.json and given line
def pipeline(json_file: str, criteria: dict, src_dir: str, output_file: str):
    lines = handle_data_flow_json(json_file, criteria)
    output_srcfile_lines(src_dir, output_file, lines)


def main():
    # the command line only supports criterion of one line
    parser = ArgumentParser()
    parser.add_argument("param1", type=str, help="slice json file path")
    parser.add_argument("-l", "--line", type=str, nargs="+", help="line number of start point e.g. main.cpp 10")
    parser.add_argument("-s", "--src", type=str, help="source file directory of project")
    parser.add_argument("-o", "--out", type=str, help="output file")

    args = parser.parse_args()
    criterion = {args.line[0]: int(args.line[1])}
    pipeline(args.param1, criterion, args.src, args.out)

if __name__ == "__main__":
    main()

