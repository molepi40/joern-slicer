import json
import os
from argparse import ArgumentParser


# load object slices from json
def load_object_slices(json_file: str):
    with open(json_file, "r") as f:
        data = f.read()
    data = json.loads(data)
    return data["objectSlices"]

def handle_usages_json(json_file: str, src_dir: str, output_file: str):
    # load object slices
    object_slices = load_object_slices(json_file)

    # load source files
    source_files = dict()
    for file_base in os.listdir(src_dir):
        with open(os.path.join(src_dir, file_base), "r") as f:
            source_files[file_base] = f.readlines()
    
    # open output file
    output_file = open(output_file, "w")


    for method_usage_slice in object_slices:
        file_name = method_usage_slice["fileName"]
        method_name = method_usage_slice["fullName"]
        output_file.write(f"file: {file_name}\n\n\n")
        output_file.write(f"method: {method_name}\n\n")

        for object_usage_slice in method_usage_slice["slices"]:
            object_defined_by = [json.loads(defined_by) for defined_by in object_usage_slice["definedBy"]]
            target_object = json.loads(object_usage_slice["targetObj"])

            object_name = target_object["name"]
            object_line = target_object["lineNumber"]
            output_file.write(f"name: {object_name}\nline number: {str(object_line)}\n")

            output_file.write("```\n")
            # defined by
            for defined_by in object_defined_by:
                for line in defined_by["lineNumber"]:
                    output_file.write(str(line) + source_files[file_name][line - 1])
            output_file.write("\n")
            # arg to calls
            for arg_to_call in object_usage_slice["argToCalls"]:
                call_lines = arg_to_call["lineNumber"]
                for call_line in call_lines:
                    output_file.write(str(call_line) + source_files[file_name][call_line - 1])
            output_file.write("```\n\n")
        

def main():
    parser = ArgumentParser()
    parser.add_argument("param1", type=str, help="usages file")
    parser.add_argument("param2", type=str, help="directory of source file")
    parser.add_argument("param3", type=str, help="output file")

    args = parser.parse_args()
    handle_usages_json(args.param1, args.param2, args.param3)

if __name__ == "__main__":
    main()
