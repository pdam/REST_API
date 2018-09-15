
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko
from pexpect import pxssh


class  user(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.name=None
        self.scope=None
        self.uid=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, name ,scope ,uid  ):
            self.cmd ="cli --quiet -c  \" user-create   name %s   scope %s   uid %s  \" \n"%(name ,scope ,uid )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines() 
            return lines
        
    def user_role_show(self ):
        self.cmd ="cli --quiet -c  \" user-role-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def role_show(self ):
        self.cmd ="cli --quiet -c  \" role-show format all  layout  horizontal parsable-delim DELIM show-headers \" \n"
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

    def show(self ):
        self.cmd ="cli --quiet -c  \" user-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" user-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" user-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" user-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines

    def getUIDAssigned(self, user_name):
        try :
            return [ x['uid'] for  x in  self.show() if x['name'] == user_name ][0]
        except:
            return None


    def getRoleAssigned(self, user_name):
        try :
            role=[ x['role'] for  x in  self.user_role_show() if x['user-name'] == user_name ][0]
            role_id= [ x['id'] for  x in  self.role_show() if x['name'] == role ][0]
            return role_id
        except:
            return None

    def createUserForTesting(self, user_name):
        s = pxssh.pxssh()
        s.login (self.switch, self.uname, self.passwd)
        s.sendline ('cli --quiet')  # run a command
        s.prompt()             # match the prompt
        createUser="user-create   name %s   scope fabric   initial-role network-admin"%user_name
        s.sendline(createUser)
        s.prompt()
        s.sendline("test123")
        s.prompt()
        s.sendline("test123")
        s.prompt()

