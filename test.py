import os
from argparse import ArgumentParser
import run_joern.run as run
from slicer.evaluate_slicer import Evaluator
from slicer.error_slicer import ErrorSlicer
from slicer.bug_slicer import BugSlicer

"""
example:
    python3 test.py -h 
    
"""

def test_project(run_joern, criterion_fmt, bug_qualifier, add_dp, project_dir):

    if run_joern:
        run.run_joern(project_dir, True, [], True, ["cpg", "pdg"], "dot")

    for fmt in criterion_fmt:
        match fmt:
            case "evaluation":
                evaluator = Evaluator(project_dir)
                evaluator.slice(add_dp)
            case "cppcheck":
                err_slicer = ErrorSlicer(project_dir)
                err_slicer.slice(add_dp)
            case "report":
                bug_slicer = BugSlicer(project_dir)
                for qualifier in bug_qualifier:
                    bug_slicer.read_bug_reports(qualifier)
                bug_slicer.slice(add_dp)
        print("")


def test(run_joern, criterion_fmt, bug_qualifier, add_dp, test_dir):

    for test in os.listdir(test_dir):

        project_dir = os.path.join(test_dir, test)
        test_project(run_joern, criterion_fmt, bug_qualifier, add_dp, project_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("param1", help="directory of test cases. if -p set, it is the project directory")
    parser.add_argument("-j", "--joern", action="store_true", help="run joern")
    parser.add_argument("-p", "--project", action="store_true", help="test a single project")
    parser.add_argument("-c", "--criterion", nargs="+", default=[], help="criterion file format:  evaluation   cppcheck  report")
    parser.add_argument("-q", "--qualifier", nargs="+", default=[], help="qualifier for bug report, only available when choose report as criterion.")
    parser.add_argument("-d", "--dependency", action="store_true", help="add other dependency edges. defaults to false")
    args = parser.parse_args()

    if args.project:
        test_project(args.joern, args.criterion, args.qualifier, args.dependency, args.param1)
    else:
        test(args.joern, args.criterion, args.qualifier, args.dependency, args.param1)