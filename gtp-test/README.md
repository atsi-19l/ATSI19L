## GTP Example ##
To make testing easier, we created example environment that's easier to manage than our main test case, by modyfying MPLS Demo we found in P4 Research repository (even this readme is based on it). Because of that topology is similar (in terms of IP addresses), however, the GTP is used instead of MPLS, as shown below:
<p align="center">
  <img src="images/GTP diagram.PNG" />
</p>

## State of the project ##
On simple network architecture, GTP encapsulation works as expected. Because of P4 architecture, push_gtp is in egress part of the switch code. In effect we have to populate table with additional line, to forward packet at first by ipv4, and only s2 truly uses gtp teid.  

## Architecture ##
The project is based on following repos and networking solutions:
* P4C (P4 language compiler) - can be accessed here: https://github.com/p4lang/p4c
* Mininet (https://github.com/mininet/mininet)

This project enables the user to emulate functional network using Mininet and the P4_16 language, and involves communication with GTP-U.
## Project Details ##
* Code of our project is written in P4-16, because it's current version of the language
* Functions pop_gtp is in ingress part of the code, while push_gtp in egress, because it's logical to put those elements in those functions
* We define 3 tables connected with gtp in our code:
  * gtp_lookup used to check how we have to forward packets with gtp header
  * gtp_table that's used to check is it the endpoint of the tunnel and pop_gtp
  * fec_table, that's used to check if that ip packet have to be encapsulated into gtp
* This table format is inherited from the source MPLS-demo that we based our project on
* push_gtp function not only have to add headers, but set correct values to those fields. It was especially hard in terms of packet lengths, because definition of this field is different between protocols and invalid value could have gruesome consequences
* pop_gtp have to invalidate gtp headers
* Parser functions may be interesting case, because parse_gtp have to:
  * Copy headers above gtp, from instance intended for non-gtp to gtp instances
  * Invalidate headers we copied from, because we don't know what headers are below gtp, and there may be a case when there is no eg. UDP, and we don't want to add it.
  * Start parsing IPv4
* We decided to do our tests on simple network, because there is less that can go wrong other than our switch code, even tough we had bigger network ready in main folder of this repository
 
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

## Changelog ##
In chronological order:
* network layout and addresation project
* attempts to run mininet and pre-configuration of the environment (mininet+bmv+simple_switch)
* first tries to compile the code using p4_14 with autotranslation
* code rewritten to p4_16
* implementation problems occured - attempts to run an example with MPLS
* modification of the MPLS example to fit the project requirements (GTP)
* modified invalid routing rules
* debugging and tracing packet flow in the network in order to find bugs
* moved some logic (decapsulation) from egress to ingress block
* deparser fixes
* push_gtp function extended (fields required to fulfill header requirements)
* encapsultation fixes
* GTP parser fixes




## Acknowledgements ##
We would like to thank mr Tomasz Osiński for his understanding attitude, willingness to help, dedication and involvement in the project support.
