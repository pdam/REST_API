
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  vnet_service(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.name=None
        self.type=None
        self.scope=None
        self.vnet=None
        self.is_global=None
        self.vnet_service=None
        self.state=None
        self.gateway=None
        self.peer_node=None
        self.active_sw=None
        self.backup_interval=None
        self.last_backup=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, name ,type ,scope ,vnet ,is_global ,vnet_service ,state ,gateway ,peer_node ,active_sw ,backup_interval ,last_backup  ):
            self.cmd ="cli --quiet -c  \" vnet-service-create   name %s   type %s   scope %s   vnet %s   is_global %s   vnet_service %s   state %s   gateway %s   peer_node %s   active_sw %s   backup_interval %s   last_backup %s  \" \n"%(name ,type ,scope ,vnet ,is_global ,vnet_service ,state ,gateway ,peer_node ,active_sw ,backup_interval ,last_backup )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" vnet-service-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" vnet-service-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" vnet-service-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" vnet-service-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        