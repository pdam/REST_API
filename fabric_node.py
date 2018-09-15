from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko


class  fabric_node(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.name=None
        self.fab_name=None
        self.mgmt_ip=None
        self.mgmt_netmask=None
        self.mgmt_mac=None
        self.fab_tid=None
        self.cluster_tid=None
        self.out_port=None
        self.version=None
        self.state=None
        self.firmware_upgrade=None
        self.device_state=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0



    def create(self, name ,fab_name ,mgmt_ip ,mgmt_netmask ,mgmt_mac ,fab_tid ,cluster_tid ,out_port ,version ,state ,firmware_upgrade ,device_state  ):
            self.cmd ="cli --quiet -c  \" fabric-node-create   name %s   fab_name %s   mgmt_ip %s   mgmt_netmask %s   mgmt_mac %s   fab_tid %s   cluster_tid %s   out_port %s   version %s   state %s   firmware_upgrade %s   device_state %s  \" \n"%(name ,fab_name ,mgmt_ip ,mgmt_netmask ,mgmt_mac ,fab_tid ,cluster_tid ,out_port ,version ,state ,firmware_upgrade ,device_state )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines()
            return lines


    def show(self ):
        self.cmd ="cli --quiet -c  \" switch-local fabric-node-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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


    def delete(self,**kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)

        self.cmd ="cli --quiet -c  \" fabric-node-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines()
        return  lines


    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" fabric-node-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines()
        return lines

    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)

        self.cmd ="cli --quiet -c  \" fabric-node-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines()
        return  lines

    def getFabricSwitches(self):
        self.cmd ="cli --quiet -c  \" switch-local fabric-node-show  format  name layout  horizontal parsable-delim DELIM show-headers \" \n"
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
