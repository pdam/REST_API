
from pprint import pprint
import sys
import os
import re
import time
import keyword
import paramiko

    
class  port_config(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        self.switch=None
        self.intf=None
        self.port=None
        self.speed=None
        self.egress_rate_limit=None
        self.autoneg=None
        self.jumbo=None
        self.enable=None
        self.lacp_priority=None
        self.lacp_individual=None
        self.stp_port_cost=None
        self.stp_port_priority=None
        self.reflect=None
        self.edge_switch=None
        self.pause=None
        self.description=None
        self.loopback=None
        self.mirror_only=None
        self.lport=None
        self.rswitch_default_vlan=None
        self.port_mac_address=None
        self.trunk=None
        self.routing=None
        self.host_enable=None

        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr=self.sshclient.exec_command("uptime\n",timeout=600)
        assert len(stdout.readlines()) > 0
        
        
    
    def create(self, switch ,intf ,port ,speed ,egress_rate_limit ,autoneg ,jumbo ,enable ,lacp_priority ,lacp_individual ,stp_port_cost ,stp_port_priority ,reflect ,edge_switch ,pause ,description ,loopback ,mirror_only ,lport ,rswitch_default_vlan ,port_mac_address ,trunk ,routing ,host_enable  ):
            self.cmd ="cli --quiet -c  \" port-config-create   switch %s   intf %s   port %s   speed %s   egress_rate_limit %s   autoneg %s   jumbo %s   enable %s   lacp_priority %s   lacp_individual %s   stp_port_cost %s   stp_port_priority %s   reflect %s   edge_switch %s   pause %s   description %s   loopback %s   mirror_only %s   lport %s   rswitch_default_vlan %s   port_mac_address %s   trunk %s   routing %s   host_enable %s  \" \n"%(switch ,intf ,port ,speed ,egress_rate_limit ,autoneg ,jumbo ,enable ,lacp_priority ,lacp_individual ,stp_port_cost ,stp_port_priority ,reflect ,edge_switch ,pause ,description ,loopback ,mirror_only ,lport ,rswitch_default_vlan ,port_mac_address ,trunk ,routing ,host_enable )
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \"switch-local  port-config-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
        
        self.cmd ="cli --quiet -c  \" port-config-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    
    
    def create(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        self.cmd ="cli --quiet -c  \" port-config-create  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" port-config-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
        
