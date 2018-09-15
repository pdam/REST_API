
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  vrg(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch=None
        self.name=None
        self.scope=None
        self.num_vlans=None
        self.vlans=None
        self.ports=None
        self.num_flows=None
        self.data_bw_min=None
        self.data_bw_max=None
        self.storage_bw=None
        self.service_bw=None
        self.restricted_resources=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr  = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch ,name ,scope ,num_vlans ,vlans ,ports ,num_flows ,data_bw_min ,data_bw_max ,storage_bw ,service_bw ,restricted_resources  ):
            self.cmd ="cli --quiet -c  \" vrg-create   switch %s   name %s   scope %s   num_vlans %s   vlans %s   ports %s   num_flows %s   data_bw_min %s   data_bw_max %s   storage_bw %s   service_bw %s   restricted_resources %s  \" \n"%(switch ,name ,scope ,num_vlans ,vlans ,ports ,num_flows ,data_bw_min ,data_bw_max ,storage_bw ,service_bw ,restricted_resources )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \"switch-local  vrg-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
    
    
    def delete(self,**kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" vrg-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" vrg-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" vrg-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines

    def createVrgForTesting(self, name):
        self.cmd ="cli --quiet -c  \" vrg-create     name %s   scope   fabric    \" \n"%name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines()
        return lines


    def deleteVrgForTesting(self, name):
        self.cmd ="cli --quiet -c  \" vrg-delete     name %s      \" \n"%name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines()
        return lines


    def  deleteAllVrgs(self):
        listVrgs = [ x['name']  for  x  in  self.show()]
        [ self.deleteVrgForTesting(x) for x in   listVrgs]

