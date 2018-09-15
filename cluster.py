
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  cluster(object):
    def  __init__(self, switch , switch2 , clustername , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.switch2= switch2
        self.uname = uname
        self.clusername=clustername
        self.passwd  = passwd
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch2, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        self.cleanupAllClusters()
        self.createCluster(clustername)
        try:
            self.node1=self.getNodeIDs()[0]['cluster-node-1']
            self.node2=self.getNodeIDs()[0]['cluster-node-2']
        except:
            self.node1=0
            self.node2=0
        
    def deleteClusterByName(self,name):
        self.cmd ="cli --quiet -c  \" cluster-delete  name %s \" \n"%name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()


    def cleanupAllClusters(self):
        try:
            cllist = [ x['name'] for  x in self.show()]
            [ self.deleteClusterByName(p)  for  p in cllist ]
        except:
            pass

    def getNodeIDs(self ):
        self.cmd ="cli --quiet -c  \" cluster-info  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
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
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" cluster-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
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

    def createCluster(self, clustername):
        self.cmd ="cli --quiet -c  \" cluster-create  name %s  cluster-node-1 %s cluster-node-2 %s \" \n"%(clustername , self.switch,self.switch2)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines = stdout.readlines()
    
    

        