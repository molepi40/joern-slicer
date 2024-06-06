import os
import json
from pdg_slice import cpg_slicer

class Evaluator:
    def __init__(self, project_dir) -> None:

        print(f"create Evaluator for {project_dir}")
        self.project_dir = project_dir
        self.src_dir = os.path.join(project_dir, "src")
        self.output_dir = os.path.join(project_dir, "bench_slice_out")
        if (not os.path.exists(self.output_dir)) or os.path.isfile(self.output_dir):
            os.mkdir(self.output_dir)   

        print("read benchs:")
        evaluation_file = os.path.join(project_dir, "evaluation.json")
        if (not os.path.exists(evaluation_file)) or (not os.path.isfile(evaluation_file)):
            raise Exception("evaluation file not exist")
        print(f"    {evaluation_file}")
        with open(os.path.join(project_dir, "evaluation.json"), "r") as f:
            data = f.read()
        data = json.loads(data)
        self.benchs = data["bench"]
    
    def slice(self, add_dp):
        print("run PDG slicer")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        pdg_dir = os.path.join(self.project_dir, "pdg")
        cpg_obj = cpg_slicer.preprocess(cpg_dir, pdg_dir, add_dp)
        for bench in self.benchs:
            bench_id = bench["id"]
            criterion = bench["criterion"]
            standard_slice = bench["slice"]

            print(f"    slice fof bench {bench_id:04}")
            cpg_slicer.run_slice(cpg_obj, self.src_dir, criterion, 
                               os.path.join(self.output_dir, f"EVL_{bench_id:04}_PDGslice.log"))