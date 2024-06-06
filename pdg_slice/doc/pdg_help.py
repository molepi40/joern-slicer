#!/usr/bin/python3

import pydot
import sys

with open("pdg-help.txt", "w") as f:
    sys.stdout = f
    help(pydot)
    help(pydot.Graph)
    help(pydot.Node)
    help(pydot.Edge)
    sys.stdout.close()