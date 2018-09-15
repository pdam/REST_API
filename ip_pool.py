import random
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

from storage_pool import storage_pool
from vnet import vnet


class ip_pool(object):
    def __init__(self, switch, uname="root", passwd="test123"):
        self.switch = switch
        self.uname = uname
        self.passwd = passwd
        self.name = None
        self.vnet = None
        self.scope = None
        self.vlan = None
        self.start_ip = None
        self.end_ip = None
        self.network = None
        self.netmask = None

        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname, password=self.passwd)
        stdin, stdout, stderr = self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0

    def createDefaultIPPoolForTesting(self, name):
        testVNet ="restVNet-%d" % random.randint(0, 20000)
        subnet = random.randint(2, 200)
        start_ip =  "172.16.%d.1" % subnet
        end_ip= "172.16.%d.254" % subnet
        spool_obj =storage_pool(self.switch)
        poolName =  spool_obj.getStoragePoolForUse()
        if poolName is None:
            return None
        v= vnet(self.switch)
        ip= ip_pool(self.switch)
        ret =v.createVnetOnStoragePool(testVNet,poolName)
        pprint(ret)
        val =ip.createDefaultPool(name ,testVNet,start_ip ,end_ip ,"24")
        pprint(val)


    def createDefaultPool(self, name,  vnet,   start_ip, end_ip, netmask):
        self.cmd = "cli --quiet -c  \" ip-pool-create   name %s   vnet %s  start-ip %s   end-ip %s     netmask %s  \" \n" % (name, vnet, start_ip, end_ip, netmask)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()
        return lines


    def deleteIPPool(self, name):
        self.cmd = "cli --quiet -c  \" ip-pool-delete   name %s   \" \n" % (
        name)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines = stdout.readlines()


    def show(self):
        self.cmd = "cli --quiet -c  \" ip-pool-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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



    def cleanAll(self):
        listIPPools=[ x['name']  for   x  in  self.show()]
        [ self.deleteIPPool(x) for x in  listIPPools]


