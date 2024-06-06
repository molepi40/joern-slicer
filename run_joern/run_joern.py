import os
from shutil import rmtree
JOERN_DIR = ""

def run_joern_parse(input_dir: str, output_file: str):
    joern_parse_cmd = f"{JOERN_DIR}joern-parse --output \"{output_file}\" \"{input_dir}\""
    os.system(joern_parse_cmd)

def run_joern_export(cpg_file: str, project_dir: str, repr: str, fmt: str):
    output_dir = os.path.join(project_dir, repr)
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        rmtree(output_dir)
    joern_export_cmd = f"{JOERN_DIR}joern-export --repr {repr} --format {fmt} --out \"{output_dir}\" \"{cpg_file}\""
    os.system(joern_export_cmd)