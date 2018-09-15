from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko
from vnet import vnet


class dns(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def addDomainToDNSServerForTesting(self, dns_server_name, domain_name, dns_ip):
        self.cmd = "cli --quiet -c  \" dns-domain-add dns-name %s  domain %s    dns-ip %s   \" \n" % (
        dns_server_name, domain_name, dns_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def showDomainForDNSServer(self, dns_server_name, domain):
        self.cmd = "cli --quiet -c  \" dns-domain-show  dns-name %s   domain   %s layout  horizontal parsable-delim DELIM show-headers \" \n" % (
        dns_server_name, domain)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        assert len(lines) > 0
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

    def deleteDomainFromDNSServerForTesting(self, dns_server_name, domain_name, dns_ip):
        self.cmd = "cli --quiet -c  \" dns-domain-remove dns-name %s  domain %s    dns-ip %s   \" \n" % (
        dns_server_name, domain_name, dns_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def addInterfaceToDNSServerForTesting(self, dns_server_name,interface_ip):
        self.cmd = "cli --quiet -c  \" dns-interface-add  dns-name %s  ip  %s netmask 24  \" \n" % (dns_server_name , interface_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        nic=lines[0].replace('Added interface ', '').strip('\n')
        return nic

    def deleteInterfaceFromDNSServerForTesting(self, dns_server_name, nic):
        self.cmd = "cli --quiet -c  \" dns-interface-remove dns-name %s  nic %s  \" \n" % (dns_server_name, nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()

    def showInterfacesForDNSServer(self, dns_server_name, nic):
        self.cmd = "cli --quiet -c  \" dns-interface-show  dns-name %s   nic  %s layout  horizontal parsable-delim DELIM show-headers \" \n" % (
        dns_server_name, nic)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines)== 0:
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

    def addRecordToDNSServerForTesting(self, dns_server_name, domain_name, dns_ip, host, ip):
        self.addDomainToDNSServerForTesting(dns_server_name, domain_name, dns_ip)
        self.cmd = "cli --quiet -c  \" dns-record-add dns-name %s  domain %s  host %s   ip %s   \" \n" % (
        dns_server_name, domain_name, host, ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def showRecordForDNSServer(self, dns_server_name, hostname, domain):
        self.cmd = "cli --quiet -c  \" dns-record-show  dns-name %s   host %s.%s   layout  horizontal parsable-delim DELIM show-headers \" \n" % (
        dns_server_name, hostname, domain)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines)== 0:
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

    def deleteRecordFromDNSServerForTesting(self, dns_server_name, host):
        self.cmd = "cli --quiet -c  \" dns-record-remove dns-name %s  host %s   \" \n" % (dns_server_name, host)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def createDNSServerForTesting(self, dns_server_name, vnet_name):
        v = vnet(self.switch)
        v.createVNetForTesting(vnet_name)
        self.cmd = "cli --quiet -c  \" dns-create name %s vnet %s enable    \" \n" % (dns_server_name, vnet_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def deleteDNSServerForTesting(self, dns_server_name, vnet_name):
        v = vnet(self.switch)
        v.deleteVnet(vnet_name)
        self.cmd = "cli --quiet -c  \" dns-delete name %s   \" \n" % (dns_server_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def deleteDNSServer(self, dns_server_name):
        self.cmd = "cli --quiet -c  \" dns-delete name %s   \" \n" % (dns_server_name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def show(self):
        self.cmd = "cli --quiet -c  \" dns-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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



    def deleteAllDNSServers(self):
        dns_serverlist = [x['name'] for x in self.show()]
        [self.deleteDNSServer(x) for x in dns_serverlist]

    def createDomain(self, dns_name, domain, dns_ip):
        self.cmd = "cli --quiet -c  \" dns-domain-add dns-name %s domain %s  dns-ip %s  \" \n" % (dns_name,domain,dns_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)

    def createDNSServerForTestingWithGatewayEnabled(self, dns_name, vnet_name , interface_ip, gateway_ip):
        self.createDNSServerForTesting(dns_name, vnet_name)
        nic = self.addInterfaceToDNSServerForTesting(dns_name,interface_ip)
        self.cmd = "cli --quiet -c  \" dns-modify name %s enable gateway %s  \" \n" % (dns_name,gateway_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)


