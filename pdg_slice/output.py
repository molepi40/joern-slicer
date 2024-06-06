import os
from .type import *
from .cpg import CPGNode


def map_node_to_src(nodes_collection: set[CPGNode]) -> dict[str: list[int]]:
    """map CPG node to code line in source file
    """
    
    node_map: dict[str: set[int]] = dict()
    for node in nodes_collection:
        file_name = node.get_in_file()
        if file_name not in node_map:
            node_map[file_name] = set[int]()
        node_map[file_name].add(int(node.get_attr(CPGPropertyType.LINE_NUMBER)))
    
    for file, lines in node_map.items():
        node_map[file] = sorted(list(lines))
    
    return node_map


def output_source(src_dir: str, src_lines: dict[str: list[int]], output_file) -> None:
    """output lines of source files
    """

    output = open(output_file, "w")
    for file_name in os.listdir(src_dir):
        if file_name in src_lines:
            output.write(file_name + "\n```\n")
            src_file = os.path.join(src_dir, file_name)
            with open(src_file, "r") as f:
                source = f.readlines()
            
            last_line = 0
            code = []
            for line in src_lines[file_name]:
                if line > last_line + 1:
                    code.append("...\n")
                code.append(str(line) + "  " + source[line - 1])
                last_line = line
            output.writelines(code)
            output.write("```\n")
