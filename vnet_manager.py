from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class vnet_manager(object):
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

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def AddInterface(self, mgr_name, interface_ip):
        self.cmd = "cli --quiet -c  \" vnet-manager-interface-add vnet-manager-name  %s   ip %s \" \n" % (
        mgr_name, interface_ip)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        line = stdout.readlines()[0]
        line=line.replace('Added interface ','').strip('\n')
        return line

    def create(self, name, type, scope, vnet, is_global, vnet_service, state):
        self.cmd = "cli --quiet -c  \" vnet-manager-create   name %s   type %s   scope %s   vnet %s   is_global %s   vnet_service %s   state %s  \" \n" % (
        name, type, scope, vnet, is_global, vnet_service, state)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" vnet-manager-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

        self.cmd = "cli --quiet -c  \" vnet-manager-delete  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def create(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)
        self.cmd = "cli --quiet -c  \" vnet-manager-create  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def modify(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" vnet-manager-modify  %s  \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines
