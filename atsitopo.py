import sys
sys.path.append('../')
from mn.p4_mininet import P4Switch, P4Host
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI

import argparse

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable', type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file', type=str, action="store", required=True)
args = parser.parse_args()


class DemoTopo(Topo):
    "Demo topology"

    def __init__(self, sw_path, json_path, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        s1 = self.addSwitch('s1',
                            sw_path=sw_path,
                            json_path=json_path,
                            thrift_port=9091)
        s2 = self.addSwitch('s2',
                            sw_path=sw_path,
                            json_path=json_path,
                            thrift_port=9092)
        s3 = self.addSwitch('s3',
                            sw_path=sw_path,
                            json_path=json_path,
                            thrift_port=9093)
        s4 = self.addSwitch('s4',
                            sw_path=sw_path,
                            json_path=json_path,
                            thrift_port=9094)


        h1 = self.addHost('h1',
                          ip="10.10.10.1/30",
                          mac='00:00:00:00:00:01')
        h2 = self.addHost('h2',
                          ip="10.10.20.1/30",
                          mac='00:00:00:00:00:02')
        h3 = self.addHost('h3',
                          ip="10.10.30.1/30",
                          mac='00:00:00:00:00:03')
        h4 = self.addHost('h4',
                          ip="10.10.40.1/30",
                          mac='00:00:00:00:00:04')

        self.addLink(s1, h1)
        self.addLink(s1, h3)
        self.addLink(s3, h2)
        self.addLink(s3, h4)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s1, s4)
        self.addLink(s4, s3)

def main():
    topo = DemoTopo(args.behavioral_exe,
                            args.json)

    net = Mininet(topo=topo,
                  host=P4Host,
                  switch=P4Switch,
                  controller=None)
    net.start()

    s1 = net.get('s1')
    s1.setIP('10.10.10.2/30', intf = 's1-eth1')
    s1.setMAC('00:00:00:00:01:01', intf = 's1-eth1')
    s1.setIP('10.10.30.2/30', intf = 's1-eth2')
    s1.setMAC('00:00:00:00:01:02', intf = 's1-eth2')
    s1.setIP('192.168.3.1/30', intf = 's1-eth3')
    s1.setMAC('00:00:00:00:01:03', intf='s1-eth3')
    s1.setIP('192.168.1.1/30', intf = 's1-eth4')
    s1.setMAC('00:00:00:00:01:04', intf='s1-eth4')

    s2 = net.get('s2')
    s2.setIP('192.168.3.2/30', intf = 's2-eth1')
    s2.setMAC('00:00:00:00:02:01', intf='s2-eth1')
    s2.setIP('192.168.4.1/30', intf = 's2-eth2')
    s2.setMAC('00:00:00:00:02:02', intf='s2-eth2')

    s3 = net.get('s3')
    s3.setIP('10.10.20.2/30', intf='s3-eth1')
    s3.setMAC('00:00:00:00:03:01', intf='s3-eth1')
    s3.setIP('10.10.40.2/30', intf='s3-eth2')
    s3.setMAC('00:00:00:00:03:02', intf='s3-eth2')
    s3.setIP('192.168.4.2/30', intf='s3-eth3')
    s3.setMAC('00:00:00:00:03:03', intf='s3-eth3')
    s3.setIP('192.168.2.2/30', intf='s3-eth4')
    s3.setMAC('00:00:00:00:03:04', intf='s3-eth4')

    s4 = net.get('s4')
    s4.setIP('192.168.1.2/30', intf='s4-eth1')
    s4.setMAC('00:00:00:00:04:01', intf='s4-eth1')
    s4.setIP('192.168.2.1/30', intf='s4-eth2')
    s4.setMAC('00:00:00:00:04:02', intf='s4-eth2')


    h1 = net.get('h1')
    h1.setDefaultRoute("dev eth0 via 10.10.10.2")

    h2 = net.get('h2')
    h2.setDefaultRoute("dev eth0 via 10.10.20.2")

    h3 = net.get('h3')
    h3.setDefaultRoute("dev eth0 via 10.10.30.2")

    h4 = net.get('h4')
    h4.setDefaultRoute("dev eth0 via 10.10.40.2")

    print "Ready !"

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
