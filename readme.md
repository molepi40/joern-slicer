direcly run `test.py`
```
example for single test

> python3 test.py -h
> python3 test.py ./test/mytest -p -j
> python3 test.py ./test/mytest -p -d -c report -q infer csa
> python3 test.py ./test/example/npd -p -j -d -c evaluation cppcheck
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
| | - cpg
| | - csa_output
| | - infer_output
| | - pdg
| | - src
| | cpg.bin
| | cppcheck_err.xml
| | evaluation.json
| - test2
| | - src
...
```