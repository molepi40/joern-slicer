import os
import time
from argparse import ArgumentParser
from .run_joern_slice import run_slice
from .run_joern import run_joern_export, run_joern_parse, JOERN_DIR

'''
run joern for specified project
> python3 run.py -h

structure of project
project dir
  - src
  - export-dir
  cpg.bin
  data-flow.json
  usages.json
'''

def run_joern(project_dir: str, gen_cpg: bool, gen_slice: list[str], \
             gen_export: bool, export_repr: list[str], export_fmt: str):

    print(os.path.basename(project_dir))

    # if project dir exist
    if (not os.path.exists(project_dir)) or os.path.isfile(project_dir):
        raise Exception("project directory not exist.")

    # if source file dir exist
    src_dir = os.path.join(project_dir, "src")
    if (not os.path.exists(src_dir)) or os.path.isfile(src_dir):
        raise Exception("source file directory not exist.")

    # run joern
    cpg_file = os.path.join(project_dir, "cpg.bin")
    if gen_cpg:
        run_joern_parse(src_dir, cpg_file)

    # run joern-slice
    if gen_slice:
        t1 = time.time()
        for mode in gen_slice:
            run_slice(cpg_file, project_dir, mode)
        t2 = time.time()
        t = t2 - t1
        print(f"slice time: {t}s")    

    # run joern-export
    if gen_export:
        for repr in export_repr:
            run_joern_export(cpg_file, project_dir, repr, export_fmt)

     

# for single files structure
def _process_for_single(test_origin_dir: str, test_target_dir: str, gen_cpg: bool, gen_slice: str, \
                       gen_export: bool, export_repr: str, export_fmt: str):
    
    # create target dir if neccessary
    if not os.path.exists(test_target_dir):
        os.mkdir(test_target_dir)

    # handle file
    for file_name in os.listdir(test_origin_dir):
        file = os.path.join(test_origin_dir, file_name)
        if os.path.isfile(file) and (file.endswith(".c") or file.endswith(".cpp")):

            # create dir for file
            file_target_dir = os.path.join(test_target_dir, os.path.splitext(file_name)[0])
            if not os.path.exists(file_target_dir):
                os.mkdir(file_target_dir)

            # create src dir in file dir  
            file_src_target_dir = os.path.join(file_target_dir, "src")
            if not os.path.exists(file_src_target_dir):
                os.mkdir(file_src_target_dir)
            
            # copy src file to src dir
            os.system(f"cp \"{file}\" \"{file_src_target_dir}\"")

            # pipeline for one project
            run_joern(file_target_dir, gen_cpg, gen_slice, gen_export, export_repr, export_fmt)



def main():
    parser = ArgumentParser()
    parser.add_argument("param1", type=str, help="directory of project")
    parser.add_argument("-c", "--cpg", action="store_true", help="output cpg file - defaults to false")
    parser.add_argument("-s", "--slice", nargs="+", type=str, default=[], help="execute joern-slice - data-flow or usages")
    parser.add_argument("-e", "--export", action="store_true", help="export repretentation graph - defaults to false")
    parser.add_argument("-r", "--repr", nargs="+", type=str, default=[], help="representation of exported graph - defaults to all")
    parser.add_argument("-f", "--format", type=str, default="dot", help="format of exported representation graph - defaults to dot")

    args = parser.parse_args()
    run_joern(args.param1, args.cpg, args.slice, args.export, args.repr, args.format)

if __name__ == "__main__":
    main()
