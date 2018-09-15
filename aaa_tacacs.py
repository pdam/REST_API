import paramiko

    
class  aaa_tacacs(object):
    def  __init__(self, switch , uname="root" ,passwd="test123"):
        self.switch =  switch
        self.uname = uname
        self.passwd  = passwd
        
        self.sshclient =  paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(switch, username=self.uname,password=self.passwd)
        stdin, stdout, stderr =self.sshclient.exec_command("uptime\n")
        assert len(stdout.readlines()) > 0
        
    def cleanUpTatacsConfiguration(self):
        try:
            listOfConfigs = [ x['name'] for x  in  self.show()]
            [ self.deleteTacacsServerForTesting(x) for x in  listOfConfigs ]
        except:
            pass

    def create(self):
            self.cmd ="cli --quiet -c  \" aaa-tacacs-create   \" \n"%()
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines() 
            return lines
        
    def  createTacacsServerForTesting(self, tacacs_name , tacacs_server="10.20.18.221"):
            self.cmd ="cli --quiet -c  \" aaa-tacacs-create name   %s   server %s    scope fabric  \" \n"%(tacacs_name ,tacacs_server)
            stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            return lines

    def  deleteTacacsServerForTesting(self, tacacs_name ):
            self.cmd ="cli --quiet -c  \" aaa-tacacs-delete name   %s   \" \n"%(tacacs_name )
            stdin, stdout, stderr= self.sshclient.exec_command(self.cmd,timeout=600)
            lines=stdout.readlines()
            return lines


    def show(self ):
        self.cmd ="cli --quiet -c  \" aaa-tacacs-show  layout  horizontal parsable-delim DELIM show-headers \" \n"
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
    
    
    def delete(self,**kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" aaa-tacacs-delete  %s \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
    

    def modify(self, **kwargs ):
        self.command=""
        for k,v in kwargs.items():
            if v == True:
                self.command  += " %s " %k
            self.command  += " %s %s "% (k,v)
        
        self.cmd ="cli --quiet -c  \" aaa-tacacs-modify  %s  \" \n"% (self.command)
        stdin, stdout, stderr = self.sshclient.exec_command(self.cmd,timeout=600)
        lines=stdout.readlines() 
        return  lines
