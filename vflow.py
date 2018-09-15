
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

class  vflow(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd = passwd
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr=self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def show(self, name ):
        self.cmd ="cli --quiet -c  \" vflow-show name %s layout  horizontal parsable-delim DELIM show-headers \" \n"%name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines()
        self.headers=lines[0].strip('\n').split("DELIM")
        listentries=[]
        entries=lines[1:]
        for entry in  entries:
            ventries = entry.strip('\n').split("DELIM")
            listentries.append(dict(zip(self.headers,ventries)))
        return listentries






