
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  switch_setup(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch_name=None
        self.mgmt_ip=None
        self.mgmt_netmask=None
        self.mgmt_link_state=None
        self.mgmt_link_speed=None
        self.in_band_ip=None
        self.in_band_netmask=None
        self.gateway_ip=None
        self.dns_ip=None
        self.dns_secondary_ip=None
        self.domain_name=None
        self.ntp_server=None
        self.timezone=None
        self.date=None
        self.phone_home=None
        self.hostid=None
        self.analytics_store=None
        self.mgmt_lag=None
        self.mgmt_lacp_mode=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch_name ,mgmt_ip ,mgmt_netmask ,mgmt_link_state ,mgmt_link_speed ,in_band_ip ,in_band_netmask ,gateway_ip ,dns_ip ,dns_secondary_ip ,domain_name ,ntp_server ,timezone ,date ,phone_home ,hostid ,analytics_store ,mgmt_lag ,mgmt_lacp_mode  ):
            self.cmd ="cli --quiet -c  \" switch-setup-create   switch_name %s   mgmt_ip %s   mgmt_netmask %s   mgmt_link_state %s   mgmt_link_speed %s   in_band_ip %s   in_band_netmask %s   gateway_ip %s   dns_ip %s   dns_secondary_ip %s   domain_name %s   ntp_server %s   timezone %s   date %s   phone_home %s   hostid %s   analytics_store %s   mgmt_lag %s   mgmt_lacp_mode %s  \" \n"%(switch_name ,mgmt_ip ,mgmt_netmask ,mgmt_link_state ,mgmt_link_speed ,in_band_ip ,in_band_netmask ,gateway_ip ,dns_ip ,dns_secondary_ip ,domain_name ,ntp_server ,timezone ,date ,phone_home ,hostid ,analytics_store ,mgmt_lag ,mgmt_lacp_mode )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" switch-setup-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" switch-setup-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" switch-setup-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" switch-setup-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd)
        lines=stdout.readlines() 
        return  lines
        