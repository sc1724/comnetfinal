from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
from mininet.node import Node
from mininet.link import TCLink
from cleanup import cleanup


class Topo7(Mininet):

    def __init__(self):
        Mininet.__init__(self, link=TCLink, controller=None, cleanup=True)

        # Creating Hosts
        info("Creating nodes\n")
        r1 = self.addHost('r1', inNamespace=False)
        r2 = self.addHost('r2', inNamespace=False)
        r3 = self.addHost('r3', inNamespace=False)
        r4 = self.addHost('r4', inNamespace=False)
        r5 = self.addHost('r5', inNamespace=False)
        r6 = self.addHost('r6', inNamespace=False)
        r7 = self.addHost('r7', inNamespace=False)
        s = self.addHost('s', inNamespace=False)
        d1 = self.addHost('d1', inNamespace=False)
        d2 = self.addHost('d2', inNamespace=False)
        d3 = self.addHost('d3', inNamespace=False)

        # Establishing the links from hosts to routers
        info("Creating links\n")
        self.addLink(s, r1, intfName2='r1-eth0')
        self.addLink(r1, r2, intfName1='r1-eth1')
        self.addLink(r2, r6, intfName1='r2-eth2')
        self.addLink(r6, r7, intfName1='r6-eth3')
        self.addLink(r7, d1, intfName2='r7-eth4')

        self.addLink(r1, r3, intfName2='r1-eth5')
        self.addLink(r3, r4, intfName2='r3-eth6')
        self.addLink(r3, r5, intfName2='r3-eth7')
        self.addLink(r2, r3, intfName2='r4-eth8')

        self.addLink(r4, d2, intfName2='r4-eth9')

        self.addLink(r5, d3, intfName2='r5-eth10')

        # Setting interface ip addresses since params1 or params2 just will not work
        source = self.get('s')
        host1 = self.get('d1')
        host2 = self.get('d2')
        host3 = self.get('d3')
        router1 = self.get('r1')
        router2 = self.get('r2')
        router3 = self.get('r3')
        router4 = self.get('r4')
        router5 = self.get('r5')
        router6 = self.get('r6')
        router7 = self.get('r7')

        source.setIP('192.168.1.1/24', intf='h1-eth0')
        host1.setIP('192.168.2.1/24', intf='h2-eth0')
        host2.setIP('192.168.3.1/24', intf='h3-eth0')
        host3.setIP('192.168.4.1/24', intf='h4-eth0')

        router1.setIP('192.168.1.2/24', intf='r1-eth0')
        router1.setIP('10.0.1.0/24', intf='r1-eth1')
        router1.setIP('10.0.1.1/24', intf='r1-eth6')

        router2.setIP('10.0.1.2/24', intf='r2-eth2')

        router3.setIP('10.0.1.3/24', intf='r3-eth7')
        router3.setIP('10.0.1.4/24', intf='r3-eth8')

        router4.setIP('10.0.1.5/24', intf='r4-eth9')
        router4.setIP('10.0.1.6/24', intf='r4-eth10')

        router5.setIP('192.168.4.2/24', intf='r5-eth12')

        router6.setIP('192.168.2.2/24', intf='r6-eth4')

        router7.setIP('192.168.3.2/24', intf='r7-eth11')

        # Setting default routes for each interface
        s.cmd('ip route add default via 192.168.1.2')
        d1.cmd('ip route add default via 192.168.2.2')
        d2.cmd('ip route add default via 192.168.3.2')
        d3.cmd('ip route add default via 192.168.4.2')

        r1.cmd('sysctl net.ipv4.ip_forward=1')
        r2.cmd('sysctl net.ipv4.ip_forward=1')
        r3.cmd('sysctl net.ipv4.ip_forward=1')
        r4.cmd('sysctl net.ipv4.ip_forward=1')
        r5.cmd('sysctl net.ipv4.ip_forward=1')
        r6.cmd('sysctl net.ipv4.ip_forward=1')
        r7.cmd('sysctl net.ipv4.ip_forward=1')

    def start_network(self):
        CLI(self)


if __name__ == '__main__':
    topo = Topo7()
    topo.start_network()
    cleanup()
