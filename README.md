# ATSI19L

This is the official repository of the ATSI Project (NC&SC&JJ&MO).

**Full readme can be found in gtp-test directory [here](https://github.com/atsi-19l/ATSI19L/blob/master/gtp-test/README.md).**

This project stage consists of:
- mininet configuration with static routing rules
- GTU-P implementation (in the P4 language).

To run the test topology use:

sudo python topo.py --behavioral-exe simple_switch --json p4include/router.json

To install the flow rules use (in second terminal):

bash -x ./install_flow_rules.sh

Link to Virtual Machine that can run MPLS example from P4 Demos:
https://drive.google.com/open?id=1dBLMHRfoe6RSK03U72N9iJN2HgyTraRJ
