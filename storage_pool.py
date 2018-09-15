from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class storage_pool(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.switch = None
        self.name = None
        self.raid_type = None
        self.used = None
        self.avail = None
        self.status = None
        self.state = None

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def getStoragePoolForUse(self):
        """

        """
        try:
            return [x['name'] for x in self.show() if x['status'] == 'ok'][0]
        except:
            return None

    def create(self, switch, name, raid_type, used, avail, status, state):
        self.cmd = "cli --quiet -c  \" storage-pool-create   switch %s   name %s   raid_type %s   used %s   avail %s   status %s   state %s  \" \n" % (
            switch, name, raid_type, used, avail, status, state)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

    def show(self):
        self.cmd = "cli --quiet -c  \" storage-pool-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

        self.cmd = "cli --quiet -c  \" storage-pool-delete  %s \" \n" % (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines

