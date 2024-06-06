import os
from argparse import ArgumentParser
import run_joern.run as run
from slicer.evaluate_slicer import Evaluator
from slicer.error_slicer import ErrorSlicer
from slicer.bug_slicer import BugSlicer

"""
example:
    python3 test.py ./test/others -j -d --error data-flow pdg cpg --evaluate data-flow pdg cpg 
    
"""

def test_project(run_joern, run_evaluate, run_err, run_bug, bug_qualifier, add_dp, project_dir):

    if run_joern:
        run.run_joern(project_dir, True, [], True, ["cpg", "pdg"], "dot")

    if run_evaluate:
        evaluator = Evaluator(project_dir)
        for mode in run_evaluate:
            evaluator.slice(mode, add_dp)
    
    if run_err:
        err_slicer = ErrorSlicer(project_dir)
        for mode in run_err:
            err_slicer.slice(mode, add_dp)

    if run_bug:
        bug_slicer =  BugSlicer(project_dir)
        for qualifer in bug_qualifier:
            bug_slicer.read_bug_reports(qualifer)
        for mode in run_bug:
            bug_slicer.slice(mode, add_dp)


def test(run_joern, run_evaluate, run_err, run_bug, bug_qualifier, add_dp, test_dir):

    for test in os.listdir(test_dir):

        project_dir = os.path.join(test_dir, test)
        test_project(run_joern, run_evaluate, run_err, run_bug, add_dp, project_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("param1", help="directory of test cases. if -p set, it is the project directory")
    parser.add_argument("-j", "--joern", action="store_true", help="run joern")
    parser.add_argument("-p", "--project", action="store_true", help="test a single project")
    parser.add_argument("--evaluate", nargs="+", default=[],help="run Evaluator: data-flow or pdg or cpg. need evaluation.json file in project directory.")
    parser.add_argument("--error", nargs="+", default=[], help="run ErrorSlicer: data-flow or pdg or cpg. need cppcheck_err.xml file in project directory.")
    parser.add_argument("--bug", nargs="+", default=[], help="run BugSlicer: pdg or cpg. need bug report directory in project directory.")
    parser.add_argument("--qualifier", nargs="+", default=[], help="qualifier for bug report, only available when run BugSlicer.")
    parser.add_argument("-d", "--dependency", action="store_true", help="add other dependency edges, only for cpg and dpg")
    args = parser.parse_args()

    if args.project:
        test_project(args.joern, args.evaluate, args.error, args.bug, args.qualifier, args.dependency, args.param1)
    else:
        test(args.joern, args.evaluate, args.error, args.bug, args.qualifier, args.dependency, args.param1)