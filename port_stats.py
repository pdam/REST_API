
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  port_stats(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch=None
        self.time=None
        self.port=None
        self.ibytes=None
        self.iUpkts=None
        self.iBpkts=None
        self.iMpkts=None
        self.iCongDrops=None
        self.ierrs=None
        self.obytes=None
        self.oUpkts=None
        self.oBpkts=None
        self.oMpkts=None
        self.oCongDrops=None
        self.oerrs=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch ,time ,port ,ibytes ,iUpkts ,iBpkts ,iMpkts ,iCongDrops ,ierrs ,obytes ,oUpkts ,oBpkts ,oMpkts ,oCongDrops ,oerrs  ):
            self.cmd ="cli --quiet -c  \" port-stats-create   switch %s   time %s   port %s   ibytes %s   iUpkts %s   iBpkts %s   iMpkts %s   iCongDrops %s   ierrs %s   obytes %s   oUpkts %s   oBpkts %s   oMpkts %s   oCongDrops %s   oerrs %s  \" \n"%(switch ,time ,port ,ibytes ,iUpkts ,iBpkts ,iMpkts ,iCongDrops ,ierrs ,obytes ,oUpkts ,oBpkts ,oMpkts ,oCongDrops ,oerrs )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" port-stats-show format all  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" port-stats-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" port-stats-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" port-stats-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        