# ATSI19L

This is the official repository of ATSI Project (NC&SC&JJ&MO).

This project stage consists of:
- mininet configuration with static routing rules
- GTU-P implementation (in the P4 language).

To run the test topology use:

sudo python topo.py --behavioral-exe simple_switch --json p4include/router.json

To install the flow rules use (in second terminal):

bash -x ./install_flow_rules.sh
