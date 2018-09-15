
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  acl_mac(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr=self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, acl_mac_name , src_mac , dst_mac  ):
            self.cmd ="cli --quiet -c  \" acl-mac-create name %s  action permit src-mac  %s   dst-mac  %s    scope fabric   \" \n"%(acl_mac_name , src_mac , dst_mac)
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" acl-mac-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
    
    
    def delete(self, name ):
        self.cmd ="cli --quiet -c  \" acl-mac-delete  name  %s \" \n"%(name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    
    
    def deleteAll(self):
        lMac= [x['name'] for  x in self.show()]
        print lMac
        [ self.delete(n) for n in  lMac]
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" acl-mac-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines

    def getAclId(self, acl_name):
        try :
            return [  x['id']   for  x in  self.show() if x['name'] == acl_name  ][0]
        except:
            return None
