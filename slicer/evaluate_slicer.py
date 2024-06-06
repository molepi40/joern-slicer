import os
import json
from joern_slice import data_flow
from pdg_slice import pdg_slicer
from pdg_slice import cpg_slicer

class Evaluator:
    def __init__(self, project_dir) -> None:

        print(f"create Evaluator for {project_dir}")
        self.project_dir = project_dir
        self.src_dir = os.path.join(project_dir, "src")
        self.output_dir = os.path.join(project_dir, "bench-out")
        if (not os.path.exists(self.output_dir)) or os.path.isfile(self.output_dir):
            os.mkdir(self.output_dir)   

        print("read benchs")
        evaluation_file = os.path.join(project_dir, "evaluation.json")
        if (not os.path.exists(evaluation_file)) or (not os.path.isfile(evaluation_file)):
            raise Exception("evaluation file not exist")
        with open(os.path.join(project_dir, "evaluation.json"), "r") as f:
            data = f.read()
        data = json.loads(data)
        self.benchs = data["bench"]
    
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
        for bench in self.benchs:
            criterion = bench["criterion"]
            standard_slice = bench["slice"]   

            data_flow.pipeline(data_flow_file, criterion, self.src_dir, \
                               os.path.join(self.output_dir, "data-flow-slicer-" + str(bench["id"]) + ".log"))
    
    def run_pdg_slicer(self, add_dp):
        print("run PDG slicer")
        pdg_dir = os.path.join(self.project_dir, "pdg")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        cpg_obj, pdg_obj = pdg_slicer.preprocess(cpg_dir, pdg_dir, add_dp)
        for bench in self.benchs:
            criterion = bench["criterion"]
            standard_slice = bench["slice"]

            pdg_slicer.run_slice(cpg_obj, pdg_obj, self.src_dir, criterion, 
                               os.path.join(self.output_dir, "pdg-slicer-" + str(bench["id"]) + ".log"))
    
    def run_cpg_slicer(self, add_dp):
        print("run CPG slicer")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        cpg_obj = cpg_slicer.preprocess(cpg_dir, add_dp)
        for bench in self.benchs:
            criterion = bench["criterion"]
            standard_slice = bench["slice"]

            cpg_slicer.run_slice(cpg_obj, self.src_dir, criterion, 
                               os.path.join(self.output_dir, "cpg-slicer-" + str(bench["id"]) + ".log"))