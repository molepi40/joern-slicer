import os
from argparse import ArgumentParser
from .run_joern import JOERN_DIR

'''
run joern-slice
> python3 run_joern_slice.py <data-flow|usages> <cpg file path> <output path>
'''

def _cpg_params(dummy_types=False, file_filter=None, method_name_filter=None, method_parameter_filter=None, method_annotation_filter=None):
    params = ""
    if dummy_types:
        params += f" --dummy-types"
    if file_filter is not None:
        params += f" --file-filter"
    if method_name_filter is not None:
        params += f" --method-name-filter {method_name_filter}"
    if method_parameter_filter is not None:
        params += f" --method-parameter-filter {method_parameter_filter}"
    if method_annotation_filter is not None:
        params += f" --method-annotation-filter {method_annotation_filter}"

    return params


def _run_data_flow(cpg_file, output_dir, slice_depth=5, sink_filter=None, end_at_external_method=False):
    # cpg_file = os.path.abspath(cpg_file)
    if not os.path.isfile(cpg_file):
        raise Exception(f"cpg file not exist in {os.path.dirname(cpg_file)}")
    
    # add paras
    joern_slice_instr = f"{JOERN_DIR}joern-slice data-flow"
    if slice_depth != 20:
        joern_slice_instr += f" --slice-depth {slice_depth}"
    if sink_filter is not None:
        joern_slice_instr += f" --sink-filter {sink_filter}"
    if end_at_external_method:
        joern_slice_instr += f" --end-at-external-method"
    
    joern_slice_instr += _cpg_params()
    output_file = os.path.join(output_dir, "data-flow.json")
    joern_slice_instr += f" --out \"{output_file}\" \"{cpg_file}\""

    # execute
    try:
        os.system(joern_slice_instr)
    except:
        raise Exception("joern-slce failed.") 


def _run_usages(cpg_file, output_dir, min_num_calls=1, exclude_operators=False, exclude_source=False):
    # cpg_file = os.path.abspath(cpg_file)
    if not os.path.isfile(cpg_file):
        raise Exception(f"cpg file not exist in {os.path.dirname(cpg_file)}")
    
    # add params
    joern_slice_instr = f"{JOERN_DIR}joern-slice usages"
    if min_num_calls > 1:
        joern_slice_instr += f" --min_num_calls {min_num_calls}"
    if exclude_operators:
        joern_slice_instr += f" --exclude-operators"
    if exclude_source:
        joern_slice_instr += f" --exclude_source"

    joern_slice_instr += _cpg_params()
    output_file = os.path.join(output_dir, "usages.json")
    joern_slice_instr += f" --out \"{output_file}\" \"{cpg_file}\""

    # execute
    try:
        os.system(joern_slice_instr)
    except:
        raise Exception("joern-slce failed.")


def run_slice(cpg_file, output_dir, mode):
    if mode == "data-flow":
        _run_data_flow(cpg_file, output_dir)
    elif mode == "usages":
        _run_usages(cpg_file, output_dir)
    else:
        raise Exception("joern slicer command error.")


def _main():
    parser = ArgumentParser()
    parser.add_argument("param1", type=str, help="slicing mode")
    parser.add_argument("param2", type=str, help="cpg file")
    parser.add_argument("param3", type=str, help="output dir")
    args = parser.parse_args()

    if args.param1 == "data-flow":
        _run_data_flow(args.param2, args.param3)
    elif args.param1 == "usages":
        _run_usages(args.param2, args.param3)
    else:
        raise Exception("wrong parameters.")

if __name__ == "__main__":
    _main()