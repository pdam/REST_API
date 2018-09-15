import json
import logging
import random
from pprint import pprint

import paramiko
import requests

from ip_pool import ip_pool
from storage_pool import storage_pool
from vnet import vnet


class dhcp(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.name = None
        self.type = None
        self.scope = None
        self.vnet = None
        self.is_global = None
        self.vnet_service = None
        self.state = None
        self.gateway = None
        self.pxe_boot = None
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def createDHCPServiceForTestingWithHostAdded(self, dhcp_name, ip_pool_name, vnet_name, host_name, mac_addr):
        self.createDHCPServiceForTesting(dhcp_name, ip_pool_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command("cli  --quiet  -c  \"dhcp-host-add dhcp-name %s hostname %s mac  %s\"  \n" % (dhcp_name, host_name, mac_addr),timeout=600)

    def createDHCPServiceForTestingWithPoolAdded(self, dhcp_name, ip_pool_name, vnet_name):
        self.createDHCPServiceForTesting(dhcp_name, ip_pool_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command(
            "cli  --quiet  -c  \"dhcp-pool-add dhcp-name %s dhcp-ip-pool %s gateway-ip 172.16.32.11 \"  \n" % (
                dhcp_name, ip_pool_name),timeout=600)

    def AddIpPoolToDHcpService(self,dhcp_name, vnet_name , ip_pool_name, start_ip,end_ip ):
        stdin, stdout, stderr = self.sshclient.exec_command(
            "cli  --quiet  -c  \"ip-pool-create name %s  vnet %s start-ip %s end-ip %s netmask 24  \"  \n" % (
                 ip_pool_name,vnet_name,start_ip,end_ip),timeout=600)
        stdin, stdout, stderr = self.sshclient.exec_command(
            "cli  --quiet  -c  \"dhcp-pool-add dhcp-name %s dhcp-ip-pool %s  \"  \n" % (
                dhcp_name, ip_pool_name),timeout=600)




    def createDHCPServiceForTestingWithInterfaceAdded(self, dhcp_name, ip_pool_name, vnet_name, interface_ip):
        self.createDHCPServiceForTesting(dhcp_name, ip_pool_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command(
                "cli  --quiet  -c  \"dhcp-interface-add  dhcp-name   %s if  data ip  %s netmask 24\"  \n" % (
                    dhcp_name, interface_ip),timeout=600)
        nic =stdout.readlines()[0].replace('Added interface ' , '').strip('\n')
        return nic

    def createDHCPServiceForTestingWithPxeMenuAdded(self, dhcp_name, ip_pool_name, vnet_name, pxe_menu):
        self.createDHCPServiceForTesting(dhcp_name, ip_pool_name, vnet_name)
        pxe_menu_name, iso_label,menu_label, kernel_iso_path, initrd_iso_path,append= self.getPxeMenuForDHCPService(dhcp_name)
        cmd="cli  --quiet  -c  \"dhcp-pxe-menu-add dhcp-name %s  name %s  iso-label %s kernel-iso-path %s initrd-iso-path %s append ks=http://<server-ip>:<web-port>/kickstarts/ubuntu.ks \"  \n" % (dhcp_name, pxe_menu,iso_label,kernel_iso_path,initrd_iso_path)
        stdin, stdout, stderr = self.sshclient.exec_command(cmd,timeout=600)

    def createDHCPService(self, dhcp_name, ip_pool_name, vnet_name):
        stdin, stdout, stderr = self.sshclient.exec_command(
            "cli  --quiet  -c  \"dhcp-create name %s  vnet %s initial-ip-pool %s \" \n" % (
            dhcp_name, vnet_name, ip_pool_name),timeout=600)
        pprint([x for x in self.show() if x['name'] == dhcp_name])

    def deleteDHCPServiceForTesting(self, dhcp_name, ip_pool_name, vnet_name):
        vnetobj = vnet(self.switch)
        vnetobj.deleteVnet(vnet_name)
        ippoolobj = ip_pool(self.switch)
        ippoolobj.deleteIPPool(ip_pool_name)
        dhcpobj = dhcp(self.switch)
        dhcpobj.deleteDHCPService(dhcp_name)

    def getNicDHCPServiceInterface(self, dhcp_name):
        listIf = self.showByFilter("interface")
        return [x['nic'] for x in listIf if x['dhcp-name'] == dhcp_name][0]

    def createDHCPServiceForTesting(self, dhcp_name, ip_pool_name, vnet_name):
        s = storage_pool(self.switch)
        subnet = random.randint(2, 200)
        start_ip = "172.16.%d.1" % subnet
        end_ip = "172.16.%d.254" % subnet
        v = vnet(self.switch)
        ip = ip_pool(self.switch)
        ret = v.createVNetForTesting(vnet_name)
        pprint(ret)
        val = ip.createDefaultPool(ip_pool_name, vnet_name, start_ip, end_ip, "24")
        pprint(val)
        self.createDHCPService(dhcp_name, ip_pool_name, vnet_name)

    def showByFilter(self, filter):
        self.cmd = "cli --quiet -c  \" dhcp-%s-show  layout  horizontal parsable-delim DELIM show-headers \" \n" % filter
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

    def show(self):
        self.cmd = "cli --quiet -c  \" dhcp-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def deleteDHCPService(self, name):
        self.cmd = "cli --quiet -c  \"dhcp-delete  name %s \" \n" % name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def cleanAll(self):
        listDhcpServices = [x['name'] for x in self.show()]
        [self.deleteDHCPService(x) for x in listDhcpServices]

    def getPxeMenuForDHCPService(self, dhcp_service_name):
        listIf = self.showByFilter("pxe-menu")
        return [( x['name'] ,  x['iso-label'] , x['menu-label'] , x['kernel-iso-path'] , x['initrd-iso-path'] , x['append'] )for x in listIf if x['dhcp-name'] == dhcp_service_name][0]

    def showDHCPHosts(self):
        self.cmd = "cli --quiet -c  \" dhcp-host-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def showDHCPPools(self):
        self.cmd = "cli --quiet -c  \" dhcp-pool-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def showDHCPPxeMenus(self):
        self.cmd = "cli --quiet -c  \" dhcp-pxe-menu-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def showDhcpInterfaces(self):
        self.cmd = "cli --quiet -c  \" dhcp-interface-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
