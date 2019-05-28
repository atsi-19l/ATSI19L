## GTP Example ##
To make testing easier, we created example environment that's easier to manage than our main test case, by modyfying MPLS Demo we found in P4 Research repository (even this readme is based on it). Because of that topology is exactly the same:
<p align="center">
  <img src="images/GTP diagram.PNG" />
</p>

## State of the project ##
On simple network architecture, ping work as expected. ~~Sadly, because push_gtp is in egress part of the switch code, we have to populate table with additional line, to forward packet at first by ipv4, and only s2 truly uses gtp teid.~~  
After fixes, the GTP works properly, with two minor issues:
* the header of the GTP packet indicates that the GTP-C is sent (it should be GTP-U acc. to project requirements) - checked by Wireshark
* Message Type field for user plane message should be set to 255.

## Architecture ##
The project is based on following repos and networking solutions:
* P4C (P4 language compiler) - can be accessed here: https://github.com/p4lang/p4c
* Mininet (https://github.com/mininet/mininet)

This project enables the user to emulate functional network using Mininet and the P4 language, and involves communication with GTP-U.

## User guide ##

1. First of all you need to setup the environment on your Linux machine.
2. From gtp-test/ directory run the Mininet topology with MPLS program.

`sudo python topo.py --behavioral-exe simple_switch --json p4include/gtp_p16.json`

4. In the Mininet console, check if ping between h1 and h2 works (it shouldn't!).

`h1 ping h2`

5. As expected ping doesn't work, because the static rules weren't populated by control plane. Populate static rules manually by invoking:

`./install_flow_rules.sh`

6. Now it should fully work

`h1 ping h2`

## Acknowledgements ##
We would like to thank mr Tomasz Osiński for his understanding attitude, willingness to help, dedication and involvement in the project support.
