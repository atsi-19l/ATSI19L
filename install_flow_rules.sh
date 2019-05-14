#!/usr/bin/env bash

# Install flow rules for switch S1
simple_switch_CLI --thrift-port 9091 < s1-commands

# Install flow rules for switch S2
simple_switch_CLI --thrift-port 9092 < s2-commands

# Install flow rules for switch S3
simple_switch_CLI --thrift-port 9093 < s3-commands

# Install flow rules for switch S4
#simple_switch_CLI --thrift-port 9094 < s4-commands
