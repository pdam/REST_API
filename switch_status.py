from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class switch_status(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.switch = None
        self.name = None
        self.value = None
        self.units = None
        self.state = None

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)

    def create(self, switch, name, value, units, state):
        self.cmd = "cli --quiet -c  \" switch-status-create   switch %s   name %s   value %s   units %s   state %s  \" \n" % (
        switch, name, value, units, state)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" switch-status-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        assert len(lines) > 0
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]

        listentries = []
        entries = lines[1:]
        for entry in entries:
            ventries = entry.strip('\r\n').split("DELIM")
            count=0
            tmpDict={}
            for  header in self.headers:
                  val= ventries[count]
                  if header != '':
                    tmpDict[header]= val
                  count+=1
            listentries.append(tmpDict)
        return listentries

    def delete(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" switch-status-delete  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        return lines

    def create(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)
        self.cmd = "cli --quiet -c  \" switch-status-create  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def modify(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" switch-status-modify  %s  \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines



