import random
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class bootenv(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.name = None
        self.version = None
        self.current = None
        self.reboot = None
        self.space = None
        self.created = None

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0

    def currentBootEnvByName(self):
        cliList = self.show()
        pprint(cliList)
        currName = [x['name'] for x in cliList if x['current'] == 'yes'][0]
        return currName

    def getExistingBootName(self):
        cliList = self.show()
        pprint(cliList)
        existingName = [x['name'] for x in cliList if x['current'] == 'no'][0]
        return existingName

    def create(self, name, version, current, reboot, space, created):
        self.cmd = "cli --quiet -c  \" bootenv-create   name %s   version %s   current %s   reboot %s   space %s   created %s  \" \n" % (
        name, version, current, reboot, space, created)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" bootenv-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
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

    def delete(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" bootenv-delete  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        return lines



    def modify(self, **kwargs):
        self.command = ""
        for k, v in kwargs.items():
            if v == True:
                self.command += " %s " % k
            self.command += " %s %s " % (k, v)

        self.cmd = "cli --quiet -c  \" bootenv-modify  %s  \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        return lines
