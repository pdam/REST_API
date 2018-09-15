from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class vlan(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.switch = None
        self.id = None
        self.scope = None
        self.description = None
        self.active = None
        self.stats = None
        self.ports = None
        self.untagged_ports = None
        self.active_edge_ports = None

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr  = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def createVlanForTesting(self, id):
        self.cmd = "cli --quiet -c  \" vlan-create  id %d   scope local   description description-%d    \" \n" % (
        id, id)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readline()
        return lines

    def createVlanForTestingWithPorts(self, id, ports):
        self.createVlanForTesting(id)
        self.cmd = "cli --quiet -c  \" vlan-port-add vlan-id %d   ports %s    \" \n" % (id, ports)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readline()
        return lines

    def create(self, id, scope, ports):
        self.cmd = "cli --quiet -c  \" vlan-create  id %d   scope %s   description description-%d  ports %s   \" \n" % (
        id, scope, id, ports)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readline()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" switch-local  vlan-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def delete(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" vlan-delete  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def modify(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" vlan-modify  %s  \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def cleanupVlans(self):
        listVlan = [x['id'] for x in self.show()]
        [self.deleteVlanById(v) for v in listVlan]

    def deleteVlanById(self, v):
        self.cmd = "cli --quiet -c  \" vlan-delete  id %s \" \n"%v
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
