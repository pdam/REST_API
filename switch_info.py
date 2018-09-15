
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  switch_info(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch=None
        self.model=None
        self.chassis_serial=None
        self.cpu1_type=None
        self.cpu2_type=None
        self.system_mem=None
        self.switch_device=None
        self.polaris_device=None
        self.gandalf_version=None
        self.fan1_status=None
        self.fan2_status=None
        self.fan3_status=None
        self.fan4_status=None
        self.ps1_status=None
        self.ps2_status=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch ,model ,chassis_serial ,cpu1_type ,cpu2_type ,system_mem ,switch_device ,polaris_device ,gandalf_version ,fan1_status ,fan2_status ,fan3_status ,fan4_status ,ps1_status ,ps2_status  ):
            self.cmd ="cli --quiet -c  \" switch-info-create   switch %s   model %s   chassis_serial %s   cpu1_type %s   cpu2_type %s   system_mem %s   switch_device %s   polaris_device %s   gandalf_version %s   fan1_status %s   fan2_status %s   fan3_status %s   fan4_status %s   ps1_status %s   ps2_status %s  \" \n"%(switch ,model ,chassis_serial ,cpu1_type ,cpu2_type ,system_mem ,switch_device ,polaris_device ,gandalf_version ,fan1_status ,fan2_status ,fan3_status ,fan4_status ,ps1_status ,ps2_status )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \"switch-local  switch-info-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
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
        
        self.cmd ="cli --quiet -c  \" switch-info-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" switch-info-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" switch-info-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
        
