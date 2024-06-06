direcly run `test.py`
```
example

> python3 test.py -h
> python3 test.py ./mytest -p -j
> python3 test.py ./mytest -p -d --bug pdg cpg --qualifier infer
> python3 test.py ./test/others -j -d --error data-flow pdg cpg --evaluate data-flow pdg cpg
> python3 test.py ./test/others/npd -j -d -p --error data-flow pdg cpg --evaluate data-flow pdg cpg
```

The structure of test directory must follow the example as  
```
- test
| - test1
| | - src
| - test2
| | - src
...
```
The complete structure is as the example as
```
- test
| - test1
| | - bench-out
| | - cpg
| | - csa_output
| | - csa_slice_output
| | - error-out
| | - pdg
| | - src
| | cpg.bin
| | cppcheck_err.xml
| | data-flow.json
| | evaluation.json
| | usages.json
| - test2
| | - src
...
```