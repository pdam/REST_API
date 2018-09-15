import random
from pprint import pprint

import paramiko

    
class  acl_ip(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        

    def  createACLIPForTesting(self,acl_ip_name):
        self.create( acl_ip_name , "192.168.1.%d"%random.randint(2,200) ,"192.168.21.%d"%random.randint(2,200) )

    
    def create(self, acl_ip_name , src_ip , dest_ip ):
            self.cmd ="cli --quiet -c  \" acl-ip-create name %s  action permit scope fabric src-ip  %s src-ip-mask  24   dst-ip %s  dst-ip-mask  24 \" \n"%(acl_ip_name , src_ip , dest_ip)
            pprint(self.cmd)
            stdin, stdout, stderr  = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            pprint(lines)
            return lines
        
    
    def show(self ):
        self.cmd ="cli --quiet -c  \" acl-ip-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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


    def deleteAll(self):
        lMac= [x['name'] for  x in self.show()]
        print lMac
        [ self.delete(n) for n in  lMac]
    
    def delete(self,name):
        self.cmd ="cli --quiet -c  \" acl-ip-delete name  %s \" \n"% name
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    
    
    def createCli(self, src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,dst_ip,port ):
        self.cmd ="cli --quiet -c  \" acl-ip-create  name  %s src-ip-mask %s  proto %s  vlan   %s src-port  %s dst-ip-mask %s src-ip %s dst-port %s action permit  scope fabric dst-ip %s port %s\" \n"% (src_ip_mask,name,proto,vlan,src_port,dst_ip_mask,src_ip,dst_port,dst_ip,port )
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return lines
    
    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" acl-ip-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines

    def getAclId(self, acl_name):
        try :
            return [  x['id']   for  x in  self.show() if x['name'] == acl_name  ][0]
        except:
            return None
