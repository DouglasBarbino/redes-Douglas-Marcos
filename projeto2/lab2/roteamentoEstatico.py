# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#!/usr/bin/python

from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.node import Node
from router import Router
from time import sleep

import sys
import os

class Topo(Topo):

    def __init__(self):
        super(Topo,self).__init__()
        r1 = self.addNode('r1', cls=Router, ip='192.168.0.249/30',
            defaultRoute='via 192.168.0.251')
        r2 = self.addNode('r2', cls=Router, ip='192.168.0.250/30',
            defaultRoute='via 192.168.0.251')
        
        h1_1 = self.addHost('h1-1', ip='192.168.1.1/24',
            defaultRoute='via 192.168.1.254')
        h1_2 = self.addHost('h1-2', ip='192.168.1.2/24',
            defaultRoute='via 192.168.1.254')
        h2_1 = self.addHost('h2-1', ip='192.168.2.1/24',
            defaultRoute='via 192.168.2.254')
        h2_2 = self.addHost('h2-2', ip='192.168.2.2/24',
            defaultRoute='via 192.168.2.254')
        h3_1 = self.addHost('h3-1', ip='192.168.3.1/24',
            defaultRoute='via 192.168.3.254')
        h3_2 = self.addHost('h3-2', ip='192.168.3.2/24',
            defaultRoute='via 192.168.3.254')
        h8_1 = self.addHost('h8-1', ip='192.168.8.1/24',
            defaultRoute='via 192.168.8.254')
        h8_2 = self.addHost('h8-2', ip='192.168.8.2/24',
            defaultRoute='via 192.168.8.254')
        h9_1 = self.addHost('h9-1', ip='192.168.9.1/24',
            defaultRoute='via 192.168.9.254')
        h9_2 = self.addHost('h9-2', ip='192.168.9.2/24',
            defaultRoute='via 192.168.9.254')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s8 = self.addSwitch('s8')
        s9 = self.addSwitch('s9')

        self.addLink(h1_1,s1)
        self.addLink(h1_2,s1)
        self.addLink(h2_1,s2)
        self.addLink(h2_2,s2)
        self.addLink(h3_1,s3)
        self.addLink(h3_2,s3)
        self.addLink(h8_1,s8)
        self.addLink(h8_2,s8)
        self.addLink(h9_1,s9)
        self.addLink(h9_2,s9)

        self.addLink(r1, r2)#, params2={'ip' : '10.0.0.1/8'})
        self.addLink(s1, r1)#, params2={'ip' : '192.168.1.1/24'})
        self.addLink(s2, r1)#, params2={'ip' : '192.168.2.1/24'})
        self.addLink(s3, r1)#, params2={'ip' : '192.168.3.1/24'})
        self.addLink(s8, r2)
        self.addLink(s9, r2)

def run():
    os.system("rm -f /tmp/zebra*.log /tmp/ripd*.log  /tmp/zebra*.pid /tmp/ripd*.pid logs/*")
    os.system("mn -c > /dev/null 2>&1")
    os.system("killall -9 zebra ripd ospfd > /dev/null 2>&1")
    topo= Topo()
    net = Mininet(topo=topo)
    net.start()

    r1= net.getNodeByName('R1')
    print "Starting zebra on r1"
    r1.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-R1.conf -d -i /tmp/zebra-r1.pid > logs/lab2-zebra-r1-stdout 2>&1")
    r1.waitOutput()

    print "Starting RIP on r1"
    r1.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-R1.conf -d -i /tmp/ripd-r1.pid > logs/lab2-ospf-r1-stdout 2>&1")
    r1.waitOutput()

    r2= net.getNodeByName('R2')
    print "Starting zebra on r2"
    r2.cmd("sudo /usr/lib/quagga/zebra -f /etc/quagga/conf/zebra-R2.conf -d -i /tmp/zebra-r2.pid > logs/lab2-zebra-r2-stdout 2>&1")
    r2.waitOutput()

    print "Starting RIP on r2"
    r2.cmd("sudo /usr/lib/quagga/ospfd -f /etc/quagga/conf/ospf-R2.conf -d -i /tmp/rip-r2.pid > logs/lab2-ospf-r2-stdout 2>&1")
    r2.waitOutput()

    CLI(net)
    net.stop()
    
    print "killing zebras ... RIP :c"   
    os.system("killall -9 zebra ripd ospfd")


if __name__ == '__main__':
    setLogLevel('info')
    run()