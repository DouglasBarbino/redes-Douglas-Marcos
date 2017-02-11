#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.util import dumpNodeConnections, quietRun, moveIntf
from mininet.cli import CLI
from mininet.node import Switch, OVSKernelSwitch

from subprocess import Popen, PIPE, check_output
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import termcolor as T
import time

setLogLevel('info')

parser = ArgumentParser("Configure simple BGP network in Mininet.")
parser.add_argument('--rogue', action="store_true", default=False)
parser.add_argument('--sleep', default=3, type=int)
args = parser.parse_args()

FLAGS_rogue_as = args.rogue

def log(s, col="green"):
    print T.colored(s, col)
    
class Router(Switch):
    """Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.

    """
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    @staticmethod
    def setup():
        return

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()

    def log(self, s, col="magenta"):
        print T.colored(s, col)

class SimpleTopo(Topo):
    """Topologia com 3 roteadores, 6 switchs e 12 hosts"""
    def __init__(self):
        # Add default members to class.
        super(SimpleTopo, self ).__init__()
        routers = []
        nro_roteadores = 3
        nro_switchs = 4
        nro_hosts_por_switch = 2
        for i in xrange(nro_roteadores):
            #Cria roteadores
            router = self.addSwitch('R%d' % (i+1))
            routers.append(router)
        #switchs = []
        #Dividido em duas partes pelo roteador do meio ter um switch a mais
        for s in xrange(2):
            router = 'R%d' % (s+1)
            #Cria switchs, o adiciona no vetor e faz a ligacao com o roteador
            switch = self.addSwitch('S%d' % (s+1))
            #switchs.append(switch)
            self.addLink(switch, router)
        for s in xrange(2):
            router = 'R%d' % (s+2)
            #Cria switchs, o adiciona no vetor e faz a ligacao com o roteador
            switch = self.addSwitch('S%d' % (s+3))
            #switchs.append(switch)
            self.addLink(switch, router)
        hosts = []
        for s in xrange(nro_switchs):
            switch = 'S%d' % (s+1)
            for i in xrange(nro_hosts_por_switch):
                #Cria host, o adiciona no vetor e faz a ligacao com o Switch
                host = self.addNode('H%d-%d' % (s+1, i+1)
                hosts.append(host)
                self.addLink(switch, host)
        return


def getIP(hostname):
    AS, indice = hostname.replace('H', '').split('-')
    AS = int(AS)
    indice = int(indice)
    ip = '2001:DB8:CAFE:%s::%s' % (AS, indice)
    return ip


def getGateway(hostname):
    AS, indice = hostname.replace('H', '').split('-')
    AS = int(AS)
    gw = '2001:DB8:CAFE:%s::FFFE' % (AS)
    return gw

def main():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    os.system('pgrep -f webserver.py | xargs kill -9')

    net = Mininet(topo=SimpleTopo(), switch=Router)
    net.start()
    for router in net.switches:
        if (router.name[0] == 'R'):
            router.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
            router.waitOutput()

    log("Waiting %d seconds for sysctl changes to take effect..."
        % args.sleep)
    sleep(args.sleep)

    for router in net.switches:
        if (router.name[0] == 'R'):
            router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
            router.waitOutput()
            '''router.cmd("/usr/lib/quagga/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (router.name, router.name, router.name), shell=True)
            router.waitOutput()'''
            log("Starting zebra on %s" % router.name)
            
    for host in net.hosts:
        host.cmd("ifconfig %s-eth0 %s" % (host.name, getIP(host.name)))
        host.cmd("route add default gw %s" % (getGateway(host.name)))

    CLI(net)
    net.stop()
    os.system("killall -9 zebra bgpd")
    os.system('pgrep -f webserver.py | xargs kill -9')


if __name__ == "__main__":
    main()
