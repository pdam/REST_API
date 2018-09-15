import json
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko
import requests
from pexpect import pxssh

from storage_pool import storage_pool


class  vnet(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.name=None
        self.scope=None
        self.vlans=None
        self.managed_ports=None
        self.admin=None
        self.vnet_mgr_name=None
        self.vnet_id =None
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

        
    def  cleanUpAllVnets(self):
        listVnets  = [x['name'] for  x  in  self.show()  ]
        [ self.deleteVnet(v)   for  v  in   listVnets ]
    
    def create(self, name ):
            self.cmd ="cli --quiet -c  \" vnet-create    name %s   scope  fabric\" \n"%(name )
            stdin, stdout, stderr= self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    def createVnetOnStoragePool(self, name, storage_pool):

            self.cmd ="cli --quiet -c  \" vnet-create   name %s   scope fabric   vnet-mgr-storage-pool  %s\" \n"%(name , storage_pool)
            stdin, stdout, stderr= self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            return lines

    def createVNetForTesting(self , vnet_name):
            s= storage_pool(self.switch)
            poolName =  s.getStoragePoolForUse()
            if poolName is None:
                return None
            else:
                self.createVnetOnStoragePool(vnet_name, poolName)

    def createVnetAndAssociatePorts(self,vnet_name , ports):
            self.createVNetForTesting(vnet_name)
            self.cmd ="cli --quiet -c  \" vnet-port-add vnet-name %s switch %s ports %s\" \n"%( vnet_name ,self.switch ,ports)
            stdin, stdout, stderr= self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            pprint(lines)
            return lines


    def deleteVnet(self, name):
            pprint("Deleting  vnet %s"%name)
            self.cmd="cli -e --quiet vnet-delete name %s "%name
            stdin, stdout, stderr= self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()



    def  getVNetIdForName(self, name):
            response = requests.get("http://%s/vRest/vnets/%s" % (self.switch, name), auth=('network-admin', 'test123'))
            assert response.status_code == 200
            self.vnet_id = [ x['id']  for  x in json.loads(response.text)["data"] if  x['name'] == name ][0]
            return self.vnet_id



    def  getVNetManagerForName(self, name):
           return [  x['name']   for  x in  self.show() if x['name'] == name  ][0]

    def show(self ):
        self.cmd ="cli --quiet -c  \" switch-local  vnet-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
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
    
    


    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" vnet-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        

