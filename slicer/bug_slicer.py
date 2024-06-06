import os
import json
from pdg_slice import cpg_slicer


class BugSlicer:

    def __init__(self, project_dir) -> None:
        print(f"create BugSlicer for {project_dir}")
        self.project_dir = project_dir
        self.src_dir = os.path.join(project_dir, "src")
        self.bug_report = dict()
    
    def read_bug_reports(self, qualifier):
        bug_dir = os.path.join(self.project_dir, f"{qualifier}_output")
        bug_reports = []
        print(f"read bug reports in {bug_dir}:")
        # read bug report in bug dir
        for bug_file in os.listdir(bug_dir):
            bug_file = os.path.join(bug_dir, bug_file)
            bug_reports.append(BugSlicer._read_bug_report(bug_file))

        self.bug_report[qualifier] = bug_reports
    
    def _read_bug_report(bug_file) -> dict[str, set[tuple]]: 
        print(f"    {bug_file}")
        with open(bug_file, "r") as f:
            report = json.loads(f.read())
        
        bug_report: dict = dict()
        bug_report["bug_id"] = report["bug_id"]

        criterion: dict[str, set[tuple]] = dict()
        for trace in report["Trace"]:
            if trace["filename"] not in criterion:
                criterion[trace["filename"]] = set()
            criterion[trace["filename"]].add((int(trace["line_number"]), int(trace["column_number"])))
        bug_report["criterion"] = criterion

        return bug_report

    def slice(self, add_dp):
        print("run PDG slicer")
        cpg_dir = os.path.join(self.project_dir, "cpg")
        pdg_dir = os.path.join(self.project_dir, "pdg")
        cpg_obj = cpg_slicer.preprocess(cpg_dir, pdg_dir, add_dp)

        for qualifier in self.bug_report:
            print(qualifier)
            output_dir = os.path.join(self.project_dir, f"{qualifier}_slice_output")
            if (not os.path.exists(output_dir)) or os.path.isfile(output_dir):
                os.mkdir(output_dir)
            
            for bug_report in self.bug_report[qualifier]:
                bug_id = bug_report["bug_id"]
                print(f"    slice for bug {bug_id}")
                criterion = bug_report["criterion"]

                cpg_slicer.run_slice(cpg_obj, self.src_dir, criterion, 
                                    os.path.join(output_dir, f"Bug_{bug_id:04}_PDGslice.log")) 
