
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  switch_vnic(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def createVnicForTesting(self, ip_address ,netmask=24 ):
            self.cmd ="cli --quiet -c  \" switch-vnic-create  ip %s   netmask %s   \" \n"%(ip_address,netmask)
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            line=stdout.readlines()[0]
            vnic=line.replace('Added interface ' , '').strip('\n')
            return vnic


    def deleteVnic(self, vnic ):
            self.cmd ="cli --quiet -c  \" switch-vnic-delete  nic  %s    \" \n"%(vnic)
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines()
        

    def cleanUpVnics(self):
        listNics =[ x['nic']   for x    in self.show()]
        [ self.deleteVnic(x) for x in listNics]

    def show(self ):
        self.cmd ="cli --quiet -c  \" switch-vnic-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
        if len(lines) == 0 :
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
        
        self.cmd ="cli --quiet -c  \" switch-vnic-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" switch-vnic-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" switch-vnic-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        