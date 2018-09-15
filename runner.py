import paramiko
import time
import sys,os
from vnet import vnet
from pprint import pprint
switch=sys.argv[1]
sshclient =  paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshclient.connect(switch, username="root",password="test123")
stdin, stdout, stderr =sshclient.exec_command("cli --quiet software-show\n")
con=stdout.readlines()[0].split(':')[1].strip()
x="Switch : %s ,  %s"%(switch,con)
testList  = [filename for filename in os.listdir('.') if filename.startswith("test")]
pprint(testList)
if not os.path.exists("results"):
    os.makedirs("results")
for  s in testList:
        os.system("python -m  pytest   -v %s --switch=%s  --junit-xml=results/result-%s.xml"%( s,switch,s[:-3]))
os._exit(0)

