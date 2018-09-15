
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  vlag(object):
    def  __init__(self, switch , uname="root" ,passwd="test123" ):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("cli --quiet -c \"fabric-node-show  layout  horizontal parsable-delim DELIM show-headers \" \n",timeout=600)
        lines=stdout.readlines()
        listentries=[]
        self.headers = [x for x in lines[0].strip('\r\n').split("DELIM")]
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
        self.switch=listentries[0]['name']
        self.switch2=listentries[1]['name']
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(self.switch2, username=self.uname,password=self.passwd)
        stdin, stdout, stderr  = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0
        self.cmd ="cli --quiet -c  \" cluster-show   \" \n"%()
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines()
        if len(lines)==0:
            self.cmd="cli --quiet -c  \" cluster-create name testCluster cluster-node-1 %s cluster-node-2 %s \"\n"%(self.switch ,self.switch2)
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            self.cmd ="cli --quiet -c  \" cluster-show   \" \n"
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            assert len(lines) >  0


    
    def show(self ):
        self.cmd ="cli --quiet -c  \" switch-local vlag-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        if len(lines) == 0:
            return []
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
    

    

    def createVlagForTesting(self, name, port, peer_port):
        self.cmd ="cli --quiet -c  \" vlag-create name %s  port %d  peer-port %d lacp-mode active \" \n"%(name,port,peer_port)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()


    def cleanupAllVlags(self):
        listVlags =[  x['name']   for  x   in self.show()]
        [ self.deleteVLagByName(n) for  n in  listVlags ]

    def deleteVLagByName(self, name):
        self.cmd ="cli --quiet -c  \" vlag-delete name %s   \" \n"%(name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        

