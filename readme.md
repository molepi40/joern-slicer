# joern-slicer

This is a simple slicer based on CPG and PDG exported by [joern](https://docs.joern.io/). Before you use this tool you have to ensure that joern has been installed and fill the right path of joern in `./run_joern/run_joern.py`.

The slicer support 3 kinds of criterion format `evaluation.json`, `cppcheck_err.xml` and `BUG_*.json`. You can check them in some of the test cases in `./test`. Of course you can just create your own format and use interface provided by `pdg_slice` to do the slice as you want. Glance at the slicer in `./slicer` to know the usage of the interface, bug do not forget to analyaze the source code with joern first.

If you just want to follow my structure of test cases, direcly run `test.py` to launch the slicer.
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