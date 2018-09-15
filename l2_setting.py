
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  l2_setting(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch=None
        self.aging_time=None
        self.l2_max_count=None
        self.l2_cur_count=None
        self.l2_active_count=None
        self.l2_max_mem=None
        self.l2_cur_mem=None
        self.l2_checker=None
        self.l2_checker_interval=None
        self.l3_arp_max_count=None
        self.l3_arp_cur_count=None
        self.l3_arp_max_mem=None
        self.l3_arp_cur_mem=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch ,aging_time ,l2_max_count ,l2_cur_count ,l2_active_count ,l2_max_mem ,l2_cur_mem ,l2_checker ,l2_checker_interval ,l3_arp_max_count ,l3_arp_cur_count ,l3_arp_max_mem ,l3_arp_cur_mem  ):
            self.cmd ="cli --quiet -c  \" l2-setting-create   switch %s   aging_time(s) %s   l2_max_count %s   l2_cur_count %s   l2_active_count %s   l2_max_mem %s   l2_cur_mem %s   l2_checker %s   l2_checker_interval %s   l3_arp_max_count %s   l3_arp_cur_count %s   l3_arp_max_mem %s   l3_arp_cur_mem %s  \" \n"%(switch ,aging_time ,l2_max_count ,l2_cur_count ,l2_active_count ,l2_max_mem ,l2_cur_mem ,l2_checker ,l2_checker_interval ,l3_arp_max_count ,l3_arp_cur_count ,l3_arp_max_mem ,l3_arp_cur_mem )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" l2-setting-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" l2-setting-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" l2-setting-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" l2-setting-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        