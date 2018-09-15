import random
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko
from vnet import vnet
from pexpect import pxssh

class vrouter(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.name = None
        self.type = None
        self.scope = None
        self.is_global = None
        self.vnet_service = None
        self.state = None
        self.router_type = None
        self.bgp_as = None
        self.proto_multi = None
        self.s = pxssh.pxssh()
        self.s.login (self.switch, self.uname, self.passwd)
        self.s.sendline ('cli --quiet')  # run a command
        self.s.prompt()             # match the prompt
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def close(self):
        if self.sshclient != None:
            self.sshclient.close()

    def addPrefixList(self, vrouter_name, prefix_name, action, prefix_network, sequence=123456):
        self.cmd = "cli --quiet -c  \" vrouter-prefix-list-add vrouter-name %s name   %s  action %s  prefix %s netmask  24   seq %d \" \n" % (
            vrouter_name, prefix_name, action, prefix_network, sequence)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()

    def createVRouterForPIMTestingWithGroup(self, vrouter_name, vnet_name , rp_address, rp_address2, group):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdCreateVRouter = "cli --quiet -c  \" vrouter-create name %s router-type hardware  vnet  %s  proto-multi pim-sparse\" \n" % (
            vrouter_name, vnet_name)
        stdin, stdout, stderr= self.sshclient.exec_command(self.cmdCreateVRouter,timeout=600)
        pprint(stdout.readlines())
        self.cmdAddPIMRPAdd = "cli --quiet -c  \" vrouter-pim-rp-add vrouter-name %s  rp-address %s group %s   netmask  4 \" \n" % (
            vrouter_name, rp_address,group)
        stdin, stdout, stderr= self.sshclient.exec_command(self.cmdAddPIMRPAdd,timeout=600)
        self.cmdAddPIMRPAdd2 = "cli --quiet -c  \" vrouter-pim-rp-add vrouter-name %s  rp-address %s group %s  netmask  4 \" \n" % (
            vrouter_name, rp_address2, group)
        stdin, stdout, stderr= self.sshclient.exec_command(self.cmdAddPIMRPAdd2,timeout=600)


    def createVRouterForPIMSSMTesting(self, vrouter_name, vnet_name , rp_address):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdCreateVRouter = "cli --quiet -c  \" vrouter-create name %s router-type hardware  vnet  %s  proto-multi pim-ssm\" \n" % (
            vrouter_name, vnet_name)
        stdin, stdout, stderr= self.sshclient.exec_command(self.cmdCreateVRouter,timeout=600)
        pprint(stdout.readlines())
        pprint(stderr.readlines())


    def createVRouterForPIMTesting(self, vrouter_name, vnet_name , rp_address):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdCreateVRouter = "cli --quiet -c  \" vrouter-create name %s router-type hardware  vnet  %s  proto-multi pim-sparse\" \n" % (
            vrouter_name, vnet_name)
        stdin, stdout, stderr= self.sshclient.exec_command(self.cmdCreateVRouter,timeout=600)
        pprint(stdout.readlines())
        self.cmdAddPIMRPAdd = "cli --quiet -c  \" vrouter-pim-rp-add vrouter-name %s  rp-address %s group 224.0.0.0   netmask  4 \" \n" % (
            vrouter_name, rp_address)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdAddPIMRPAdd,timeout=600)
        pprint(stdout.readlines() )
        pprint(stderr.readlines())

    def createVRouterForRipTesting(self, vrouter_name, vnet_name ,network):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.createAVRouterForTesting(vrouter_name,vnet_name )
        self.cmd = "cli --quiet -c  \" vrouter-rip-add vrouter-name %s network %s netmask  24\" \n" % (
            vrouter_name, network)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()

    def createVRouterForOSPF6Testing(self, vrouter_name,vnet_name):
        """
         First create VNET 15 and add VLAN 10 and 15
            CLI(server-switch)>vnet-create vnet v15 scope local vlans 10,15
        Then, add vRouter vr15:
            CLI(server-switch)>vrouter-create name vr15 router-type hardware  router-id 10.0.0.1 enable
        Add interfaces, 10.0.0.1 and 128.0.0.15 to the vRouter:
            CLI(server-switch)>vrouter-interface-add vrouter-name vr15 vlan 10 ip 10.0.0.1 netmask 255.255.255.0 if data
            CLI(server-switch)>vrouter-interface-add vrouter-name vr15 vlan 15 ip 128.0.0.15 netmask 255.255.255.0 if data
        Add OSPF to vRouter vr15:
            CLI(server-switch)>vrouter-ospf6-add vrouter-name vr15 nic  ospf6-area 0
            CLI(server-switch)>vrouter-ospf6-add vrouter-name vr15 network 128.0.0.0 netmask 255.255.255.0 ospf-area 0

        """

        testVLan = random.randint(4, 4000)
        testInterface = "172.16.25.%d" % random.randint(0, 200)
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdCreateVRouter = "cli --quiet -c  \" vrouter-create name %s router-type hardware  vnet  %s  router-id %s enable \" \n" % (
            vrouter_name, vnet_name, testInterface)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdCreateVRouter,timeout=600)
        pprint(stdout.readlines())
        self.cmdAdddInterfaces = "cli --quiet -c  \" vrouter-interface-add vrouter-name %s vlan %d ip %s netmask 255.255.255.0 if data \" \n" % (
            vrouter_name, testVLan, testInterface)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdAdddInterfaces,timeout=600)
        nicLine = stdout.readlines()[0]
        intfpat=re.compile("eth\d*.\d*")
        nic=re.findall(intfpat,nicLine)[0]
        pprint(nic)
        self.cmdAddOSPF6ToVRouter = "cli --quiet -c  \" vrouter-ospf6-add vrouter-name %s nic  %s  ospf6-area 0.0.0.0 \" \n" % (
            vrouter_name, nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdAddOSPF6ToVRouter,timeout=600)
        pprint(stdout.readlines())




    def createVRouterForOSPFTesting(self, vrouter_name,vnet_name, area="0"):
        """
         First create VNET 15 and add VLAN 10 and 15
            CLI(server-switch)>vnet-create vnet v15 scope local vlans 10,15
        Then, add vRouter vr15:
            CLI(server-switch)>vrouter-create name vr15 router-type hardware  router-id 10.0.0.1 enable
        Add interfaces, 10.0.0.1 and 128.0.0.15 to the vRouter:
            CLI(server-switch)>vrouter-interface-add vrouter-name vr15 vlan 10 ip 10.0.0.1 netmask 255.255.255.0 if data
            CLI(server-switch)>vrouter-interface-add vrouter-name vr15 vlan 15 ip 128.0.0.15 netmask 255.255.255.0 if data
        Add OSPF to vRouter vr15:
            CLI(server-switch)>vrouter-ospf-add vrouter-name vr15 network 10.0.0.0 netmask 255.255.255.0 ospf-area 0
            CLI(server-switch)>vrouter-ospf-add vrouter-name vr15 network 128.0.0.0 netmask 255.255.255.0 ospf-area 0

        """

        testInterface = "172.16.25.%d" % random.randint(0, 200)
        self.createAVRouterForTesting(vrouter_name,vnet_name)
        self.addInterfaceToAVRouter(vrouter_name,testInterface)
        self.cmdAddOSPFToVRouter = "cli --quiet -c  \" vrouter-ospf-add vrouter-name %s network %s netmask 255.255.255.0 ospf-area %s \" \n" % (
            vrouter_name, testInterface, area)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdAddOSPFToVRouter,timeout=600)
        pprint(stdout.readlines())

    def createVRouterForTestingWithOSPFServiceNeighbour(self, vrouter_name, vnet_name, vrouter_ip, network , vlan ,  area,clear=True):
        v = vnet(self.switch)
        if clear==True:
            v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdv = "cli --quiet -c  \"vlan-create id %d  scope local \" \n"%vlan
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdv,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware router-id %s   \" \n" % (
            vrouter_name, vnet_name, vrouter_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        pprint(stderr.readlines())
        pprint(stdout.readlines())
        self.cmd = "cli --quiet -c  \"vrouter-interface-add vrouter-name %s ip  %s netmask 24  vlan  %d \" \n" % (
            vrouter_name, vrouter_ip , vlan )
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-ospf-add vrouter-name %s  network %s netmask 24 ospf-area %d  \" \n" % (
            vrouter_name, network , area)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        pprint(stderr.readlines())
        pprint(stdout.readlines())

    def createVRouterForTestingWithOSPF6ServiceNeighbour(self, vrouter_name, vnet_name, vrouter_ip, network , vlan , clear=True):
        v = vnet(self.switch)
        if clear==True:
            v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdv = "cli --quiet -c  \"vlan-create id %d  scope local \" \n"%vlan
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdv,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware router-id %s   \" \n" % (
            vrouter_name, vnet_name, vrouter_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        pprint(stderr.readlines())
        pprint(stdout.readlines())
        nic=self.addInterfaceToAVRouter(vrouter_name,vrouter_ip)
        self.cmd = "cli --quiet -c  \" vrouter-ospf6-add vrouter-name %s  nic %s ospf6-area %s  \" \n" % (
            vrouter_name, nic , network)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        pprint(stderr.readlines())
        pprint(stdout.readlines())

    def createOSPFAreaForVrouter(self,vrouter_name ,vnet_name ,area, stub_type ):
        self.createVRouterForOSPFTesting(vrouter_name,vnet_name,area)
        self.cmd = "cli --quiet -c  \" vrouter-ospf-area-add vrouter-name %s area %s  stub-type %s  \" \n" % (
            vrouter_name, area,stub_type)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)



    def showOSPFAreaForVRouters(self):
        self.cmd = "cli --quiet -c  \" vrouter-ospf-area-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showOSPFRouters(self):
        self.cmd = "cli --quiet -c  \" vrouter-ospf-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def createAVRouterForTesting(self, vrouter_name , vnet_name):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware \" \n" % (
            vrouter_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def createAVRouterForTestingWithID(self, vrouter_name, vnet_name , router_id):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware router-id %s bgp-as 10 \" \n" % (
            vrouter_name, vnet_name, router_id)
        print (self.cmd)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def createVRouterForTestingWithBGPService(self, vrouter_name, vnet_name, vrouter_ip, neighbour):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware  router-id %s bgp-as  10  \" \n" % (
            vrouter_name, vnet_name, vrouter_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-bgp-add vrouter-name %s  neighbor %s remote-as 100  \" \n" % (
            vrouter_name, neighbour)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def createVRouterForTestingWithBGPServiceNeighbour(self, vrouter_name, vnet_name, vrouter_ip, vlan ,  neighbour,clear=True):
        v = vnet(self.switch)
        if clear==True:
            v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmdv = "cli --quiet -c  \"vlan-create id %d  scope local \" \n"%vlan
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdv,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s  vnet %s router-type hardware router-id %s bgp-as  10  \" \n" % (
            vrouter_name, vnet_name, vrouter_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        self.cmd = "cli --quiet -c  \"vrouter-interface-add vrouter-name %s ip  %s netmask 24  vlan  %d \" \n" % (
            vrouter_name, vrouter_ip , vlan )
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        self.cmd = "cli --quiet -c  \" vrouter-bgp-add vrouter-name %s  neighbor %s remote-as 100  \" \n" % (
            vrouter_name, neighbour)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        pprint(stderr.readlines())
        pprint(stdout.readlines())


    def deleteAVRouterForTesting(self, vrouter_name ):
        self.cmd = "cli --quiet -c  \" vrouter-delete   name %s   \" \n" % (vrouter_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def deleteVnetAssociatedWithVrouter(self, name):
        pprint("Deleting  vnet %s"%name)
        deleteVnet="vnet-delete   name %s "%name
        self.s.sendline(deleteVnet)
        self.s.prompt()
        self.s.sendline("y")
        self.s.prompt()



    def create(self, name, type, scope, vnet, is_global, vnet_service, state, router_type, bgp_as, proto_multi):
        self.cmd = "cli --quiet -c  \" vrouter-create   name %s   type %s   scope %s   vnet %s   is_global %s   vnet_service %s   state %s   router_type %s   bgp_as %s   proto_multi %s  \" \n" % (
            name, type, scope, vnet, is_global, vnet_service, state, router_type, bgp_as, proto_multi)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" vrouter-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showVRouterBGP(self):
        self.cmd = "cli --quiet -c  \" vrouter-bgp-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def cleanAllVRouters(self):
        listRouters = [x['name'] for x in self.show()]
        if len(listRouters) == 0:
            return
        [self.deleteAVRouterForTesting(x) for x in listRouters]

    def addStaticRoute(self, vrouter_name, network, netmask, gateway_ip):
        self.cmd = "cli --quiet -c  \" vrouter-static-route-add vrouter-name %s network %s netmask %d  gateway-ip %s distance 10 \" \n" % (
            vrouter_name, network, netmask, gateway_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()

    def showStaticRoutes(self):
        self.cmd = "cli --quiet -c  \" vrouter-static-route-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showOSPF6Routers(self):
        self.cmd = "cli --quiet -c  \" vrouter-ospf6-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showRipVRouters(self):
        self.cmd = "cli --quiet -c  \" vrouter-rip-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showVRouterBGPNeighbours(self):
        self.cmd = "cli --quiet -c  \" vrouter-bgp-neighbor-show   layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showPrefixList(self):
        self.cmd = "cli --quiet -c  \" vrouter-prefix-list-show   layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def createAVRouterForTestingWithPIMSupport(self, vrouter_name,vnet_name):
        v = vnet(self.switch)
        v.cleanUpAllVnets()
        v.create(vnet_name)
        self.cmd = "cli --quiet -c  \"vrouter-create name %s router-type hardware  vnet  %s  proto-multi pim-sparse \" \n" % (
            vrouter_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def showPIMVRouters(self):
        self.cmd = "cli --quiet -c  \" vrouter-pim-rp-show   layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showPIMVRoutersInterfaces(self):
        self.cmd = "cli --quiet -c  \" vrouter-pim-interface-show   layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def addInterfaceToAVRouter(self, vrouter_name, interface_ip):
        self.cmdv = "cli --quiet -c  \"vlan-create id 100  scope local \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdv,timeout=600)
        self.cmd = "cli --quiet -c  \"vrouter-interface-add vrouter-name %s ip  %s netmask 24 vlan 100  \" \n" % (
            vrouter_name, interface_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        nicLine = stdout.readlines()[0]
        intfpat=re.compile("eth\d*.\d*")
        nic=re.findall(intfpat,nicLine)[0]
        return nic

    def addInterfaceToAVRouterWithPIM(self, vrouter_name, interface_ip):
        self.cmdv = "cli --quiet -c  \"vlan-create id 100  scope local  \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdv,timeout=600)
        self.cmd = "cli --quiet -c  \"vrouter-interface-add vrouter-name %s ip  %s netmask 24 vlan 100 pim \" \n" % (
            vrouter_name, interface_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        nicLine = stdout.readlines()[0]
        intfpat=re.compile("eth\d*.\d*")
        nic=re.findall(intfpat,nicLine)[0]
        return nic


    def VrouterInterfaceConfigAdd(self , vrouter_name ,nic ):
        self.cmd = "cli --quiet -c  \"vrouter-interface-config-add vrouter-name %s nic %s  \" \n" % ( vrouter_name, nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def createAVrouterWithInterfaceConfigSupport(self, vrouter_name , vnet_name ,  interface_ip):
        self.createAVRouterForTesting(vrouter_name,vnet_name)
        nic=self.addInterfaceToAVRouter(vrouter_name,interface_ip)
        pprint(nic)
        self.VrouterInterfaceConfigAdd(vrouter_name,nic)
        return nic


    def addGRoupInfoToPIMVRouter(self, vrouter_name, rp_address, group):
        self.cmdAddPIMRPAdd = "cli --quiet -c  \" vrouter-pim-rp-add vrouter-name %s  rp-address %s group %s  netmask  4 \" \n" % (
            vrouter_name, rp_address, group)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdAddPIMRPAdd,timeout=600)

    def addVRouterToIGMPGroup(self, vrouter_name, interface_ip, igmp_group_name, group_ip, source_ip):
        nic = self.addInterfaceToAVRouter(vrouter_name, interface_ip)
        self.cmdaddVRouterToIGMPGroup = "cli --quiet -c  \" vrouter-igmp-static-join-add vrouter-name %s name %s  group-ip %s source-ip %s interface  %s \" \n" % (
            vrouter_name, igmp_group_name, group_ip, source_ip, nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmdaddVRouterToIGMPGroup,timeout=600)

    def createAVRouterForTestingIGMPStaticJoin(self, vrouter_name, vnet_name, interface_ip, igmp_group_name, group_ip, source_ip):
        self.createAVRouterForTesting(vrouter_name,vnet_name)
        self.addVRouterToIGMPGroup(vrouter_name, interface_ip, igmp_group_name, group_ip, source_ip)

    def showIGMPStaticGroupJoins(self):
        self.cmd = "cli --quiet -c  \"  vrouter-igmp-static-join-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showVRouterInterfaces(self):
        self.cmd = "cli --quiet -c  \"  vrouter-interface-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showPIMVRouterNeighBors(self):
        self.cmd = "cli --quiet -c  \"  vrouter-pim-neighbor-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showRoutes(self):
        self.cmd = "cli --quiet -c  \"  vrouter-routes-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showRoutesMultiCast(self):
        self.cmd = "cli --quiet -c  \"  vrouter-multicast-route-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def createAVRouterForTestingIGMPMulticast(self, vrouter_name, vnet_name):
        pass

    def showVRouterInterfacesConfigs(self):
        self.cmd = "cli --quiet -c  \"  vrouter-interface-config-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def AddLoopBackInterfaces(self, vrouter_name, interface_ip,index):
        self.cmd = "cli --quiet -c  \" vrouter-loopback-interface-add vrouter-name %s ip %s  index %s \" \n"%(vrouter_name,interface_ip,index)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()



    def showLoopbackInterfaces(self):
        self.cmd = "cli --quiet -c  \"  vrouter-loopback-interface-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def createAVRouterForTestingPacketRelay(self, vrouter_name, vnet_name, interface_ip , forward_ip ):
        self.createAVRouterForTesting(vrouter_name,vnet_name)
        nic = self.addInterfaceToAVRouter(vrouter_name,interface_ip)
        self.cmd  ="cli --quiet -c  \"  vrouter-packet-relay-add vrouter-name %s forward-proto dhcp forward-ip %s  nic %s\" \n "%(vrouter_name,forward_ip,nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        return nic


    def showPacketRelays(self):
        self.cmd = "cli --quiet -c  \"  vrouter-packet-relay-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries

    def showRIPRouters(self):
        self.cmd = "cli --quiet -c  \"  vrouter-rip-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count = 0
            tmpDict = {}
            for header in self.headers:
                val = ventries[count]
                if header != '':
                    tmpDict[header] = val
                count += 1
            listentries.append(tmpDict)
        return listentries






