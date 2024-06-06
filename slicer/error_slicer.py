import os
import xml.etree.ElementTree as ET
from joern_slice import data_flow
from pdg_slice import pdg_slicer
from pdg_slice import cpg_slicer


class Error:
    def __init__(self, error) -> None:

        self.attr = error.attrib
        self.locations: dict[str, set[tuple]] = dict()

        for location in error.findall("location"):
            file = location.get("file")
            if file not in self.locations:
                self.locations[file] = set()
            self.locations[file].add((int(location.get("line")), int(location.get("column"))))

    def get_attr(self, attr):
        return self.attr.get(attr)
    
    def get_locations(self):
        return self.locations


class ErrorSlicer:
    def __init__(self, project_dir, error_file=None) -> None:

        print(f"create ErrorSlicer for {project_dir}")
        self.project_dir = project_dir
        self.src_dir = os.path.join(project_dir, "src")
        self.ouput_dir = os.path.join(project_dir, "error-out")
        if (not os.path.exists(self.ouput_dir)) or os.path.isfile(self.ouput_dir):
            os.mkdir(self.ouput_dir)

        print("read errors")
        if not error_file:
            error_file = os.path.join(project_dir, "cppcheck_err.xml")
        if (not os.path.exists(error_file)) or (not os.path.isfile(error_file)):
            raise Exception("error file not exist")
        self.errors: set[Error] = ErrorSlicer._read_errors(error_file)      
    
    def _read_errors(error_file):
        tree = ET.parse(error_file)
        errors = list[Error]()
        for error in tree.getroot().find("errors"):
            errors.append(Error(error))
        return errors

    def slice(self, mode, add_dp=True):
        if mode == "cpg":
            self.run_cpg_slicer(add_dp)
        elif mode == "pdg":
            self.run_pdg_slicer(add_dp)
        elif mode == "data-flow":
            self.run_data_flow_slicer()

    def run_data_flow_slicer(self):
        print("run data-flow slicer")
        data_flow_file = os.path.join(self.project_dir, "data-flow.json")
        for error in self.errors:
            error_id = error.get_attr("id")
            print(f"slice {error_id}")
            criterion = error.get_locations()

            data_flow.pipeline(data_flow_file, criterion, self.src_dir, \
                               os.path.join(self.ouput_dir, "data-flow-slicer-" + error_id + ".log"))
    
    def run_pdg_slicer(self, add_dp):
        print("run PDG slicer")
        pdg_dir = os.path.join(self.project_dir, "pdg")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        cpg_obj, pdg_obj = pdg_slicer.preprocess(cpg_dir, pdg_dir, add_dp)
        for error in self.errors:
            error_id = error.get_attr("id")
            print(f"slice {error_id}")
            criterion = error.get_locations()

            pdg_slicer.run_slice(cpg_obj, pdg_obj, self.src_dir, criterion, 
                               os.path.join(self.ouput_dir, "pdg-slicer-" + error_id + ".log"))        

    def run_cpg_slicer(self, add_dp):
        print("run CPG slicer")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        cpg_obj = cpg_slicer.preprocess(cpg_dir, add_dp)
        for error in self.errors:
            error_id = error.get_attr("id")
            print(f"slice {error_id}")
            criterion = error.get_locations()

            cpg_slicer.run_slice(cpg_obj, self.src_dir, criterion, 
                               os.path.join(self.ouput_dir, "cpg-slicer-" + error_id + ".log"))